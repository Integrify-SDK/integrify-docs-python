import os

import yaml
from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin


class IntegrationsNavPlugin(BasePlugin):
    config_scheme = (
        (
            "navs_dir",
            config_options.Type(str, default="docs/az/navs"),
        ),  # folder with partial navs
    )

    def on_config(self, config: MkDocsConfig):
        navs_dir = self.config["navs_dir"]
        integration_nav = {"Integration": []}

        if not os.path.isdir(navs_dir):
            raise Exception(f"Integrations navs directory not found: {navs_dir}")

        for filename in sorted(os.listdir(navs_dir)):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                full_path = os.path.join(navs_dir, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    partial_nav = yaml.safe_load(f)
                    if not isinstance(partial_nav, dict):
                        raise ValueError(f"Invalid nav structure in: {filename}")
                    integration_nav["Integration"].append(partial_nav)

        config.nav.append(integration_nav)
        return config
