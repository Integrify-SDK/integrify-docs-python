import os
from pathlib import Path
from typing import Any, List, Union

import yaml
from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Link, Navigation, Section
from mkdocs.structure.pages import Page


class IntegrationsNavPlugin(BasePlugin):
    # folder with partial navs
    config_scheme = (("navs_dir", config_options.Type(str, default="docs/navs")),)

    def on_config(self, config: MkDocsConfig):
        navs_dir = self.config["navs_dir"]
        integrations = ["integrations/index.md"]

        if not os.path.isdir(navs_dir):
            raise Exception(f"Integrations navs directory not found: {navs_dir}")

        for filename in sorted(os.listdir(navs_dir)):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                full_path = os.path.join(navs_dir, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    partial_nav = yaml.safe_load(f)
                    if not isinstance(partial_nav, dict):
                        raise ValueError(f"Invalid nav structure in: {filename}")
                    integrations.append(partial_nav)

        config.nav.append({"Integration": integrations})
        return config


class MultiLangPlugin(BasePlugin):
    # Taken from FastAPI scripts/mkdocs_hooks.py
    def _generate_multilang_nav(
        self,
        items: List[Union[Page, Section, Link]],
        config: MkDocsConfig,
    ):
        new_items: list[Union[Page, Section, Link]] = []
        for item in items:
            if isinstance(item, Section):
                new_title = item.title
                new_children = self._generate_multilang_nav(
                    item.children,
                    config=config,
                )
                first_child = new_children[0]
                if isinstance(first_child, Page):
                    if first_child.file.src_path.endswith("index.md"):
                        # Read the source so that the title is parsed and available
                        first_child.read_source(config=config)
                        new_title = first_child.title or new_title
                # Creating a new section makes it render it collapsed by default
                # no idea why, so, let's just modify the existing one
                # new_section = Section(title=new_title, children=new_children)
                item.title = new_title.split("{ #")[0]
                item.children = new_children
                new_items.append(item)
            else:
                new_items.append(item)

        return new_items

    def on_nav(
        self,
        nav: Navigation,
        *,
        config: MkDocsConfig,
        files: Files,
        **kwargs: Any,
    ):
        new_items = self._generate_multilang_nav(nav.items, config=config)
        return Navigation(items=new_items, pages=nav.pages)

    @staticmethod
    def resolve_file(*, item: str, files: Files, config: MkDocsConfig) -> None:
        item_path = Path(config.docs_dir) / item
        if not item_path.is_file():
            en_src_dir = (Path(config.docs_dir) / "../../az/docs").resolve()
            potential_path = en_src_dir / item
            if potential_path.is_file():
                files.append(
                    File(
                        path=item,
                        src_dir=str(en_src_dir),
                        dest_dir=config.site_dir,
                        use_directory_urls=config.use_directory_urls,
                    )
                )

    def resolve_files(
        self,
        *,
        items: List[Any],
        files: Files,
        config: MkDocsConfig,
    ) -> None:
        for item in items:
            if isinstance(item, str):
                self.resolve_file(item=item, files=files, config=config)
            elif isinstance(item, dict):
                assert len(item) == 1
                values = list(item.values())
                if not values:
                    continue
                if isinstance(values[0], str):
                    self.resolve_file(item=values[0], files=files, config=config)
                elif isinstance(values[0], list):
                    self.resolve_files(items=values[0], files=files, config=config)
                else:
                    raise ValueError(f"Unexpected value: {values}")

    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        self.resolve_files(items=config.nav or [], files=files, config=config)

        if "logo" in config.theme:
            self.resolve_file(item=config.theme["logo"], files=files, config=config)
        if "favicon" in config.theme:
            self.resolve_file(item=config.theme["favicon"], files=files, config=config)

        self.resolve_files(items=config.extra_css, files=files, config=config)
        self.resolve_files(items=config.extra_javascript, files=files, config=config)
        return files


class TranslationPlaceholderPlugin(BasePlugin):
    """
    Plugin that automatically generates placeholder pages for missing translations.
    """

    config_scheme = (
        ("enabled", config_options.Type(bool, default=True)),
        (
            "languages",
            config_options.Type(dict, default={"az": "Azerbaijani", "en": "English"}),
        ),
        ("placeholder_templates", config_options.Type(dict, default={})),
    )

    def __init__(self):
        self.default_templates = {
            "az": """???+ warning
    Bu səhifənin tərcüməsi hələ ki yoxdur.

    Amma bu səhifəsi tərcumə edərək yardım edə bilərsiniz: [Contributing](https://integrify.mmzeynalli.dev/resources/contributing/){.internal-link target=_blank}.
""",
            "en": """???+ warning
    The current page still doesn't have a translation for this language.

    But you can help translating it: [Contributing](https://integrify.mmzeynalli.dev/resources/contributing/){.internal-link target=_blank}.
""",
        }

    def on_config(self, config: MkDocsConfig):
        """Initialize plugin configuration."""
        if not self.config.get("enabled", True):
            return config

        # Merge custom templates with defaults
        self.templates = {
            **self.default_templates,
            **self.config.get("placeholder_templates", {}),
        }

        return config

    def get_language_from_docs_dir(self, docs_dir: str) -> str:
        """Extract language code from docs_dir path."""
        # Check if parent directory name is a language code
        for lang_code in self.config.get("languages", {}).keys():
            if f"/{lang_code}/docs" in docs_dir or f"\\{lang_code}\\docs" in docs_dir:
                return lang_code

        return None

    def get_all_md_files(self, base_path: Path) -> set:
        """Get all markdown files in a directory, returning relative paths."""
        if not base_path.exists():
            return set()

        md_files = set()
        for md_file in base_path.rglob("*.md"):
            relative_path = md_file.relative_to(base_path)
            md_files.add(str(relative_path))
        return md_files

    def create_placeholder_content(self, lang_code: str) -> str:
        """Get placeholder content for the given language."""
        return self.templates.get(
            lang_code,
            self.templates.get(
                "en", "# Translation Missing\n\nThis page has not been translated yet."
            ),
        )

    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        """Generate placeholder files for missing translations."""
        if not self.config.get("enabled", True):
            return files

        # Get current language from docs_dir
        current_lang = self.get_language_from_docs_dir(config.docs_dir)

        if not current_lang:
            # Can't determine language, skip
            return files

        # Get the docs root (parent of language directories)
        docs_path = Path(config.docs_dir)
        docs_root = docs_path.parent.parent  # Go up from docs/xx/docs to docs/

        # Get all configured languages
        languages = self.config.get("languages", {})

        # Find files in other languages
        current_files = self.get_all_md_files(docs_path)

        for other_lang in languages.keys():
            if other_lang == current_lang:
                continue

            other_docs_path = docs_root / other_lang / "docs"
            if not other_docs_path.exists():
                continue

            other_files = self.get_all_md_files(other_docs_path)

            # Find files that exist in other language but not in current
            missing_files = other_files - current_files

            if missing_files:
                print(
                    f"\n[Translation Placeholder] Found {len(missing_files)} missing files in {current_lang}/"
                )

                for missing_file in sorted(missing_files):
                    target_path = docs_path / missing_file

                    # Create directories if they don't exist
                    target_path.parent.mkdir(parents=True, exist_ok=True)

                    # Write placeholder content
                    placeholder_content = self.create_placeholder_content(current_lang)
                    target_path.write_text(placeholder_content, encoding="utf-8")

                    # Add to files collection
                    new_file = File(
                        path=missing_file,
                        src_dir=str(docs_path),
                        dest_dir=config.site_dir,
                        use_directory_urls=config.use_directory_urls,
                    )
                    files.append(new_file)

                    print(f"  ✓ Created placeholder: {missing_file}")

        return files
