#!/bin/bash
set -e

REPO_LIST_FILE="integrations.txt"
TEMP_DIR="integrations-tmp"
LANGUAGES=("en" "az")

if [ ! -f "$REPO_LIST_FILE" ]; then
    echo "❌ $REPO_LIST_FILE not found!"
    exit 1
fi

# Clean temp and output dirs
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

DEST_SRC="src/"
rm -rf "$DEST_SRC"/integrify/*

# Clean docs for both languages
for LANG in "${LANGUAGES[@]}"; do
    DEST_DOCS="docs/$LANG/docs/"
    rm -rf "$DEST_DOCS"/integrations/*
done

echo "🔄 Starting to fetch integrations..."

while IFS= read -r REPO_URL; do
    [ -z "$REPO_URL" ] && continue  # Skip empty lines

    REPO_NAME=$(basename "$REPO_URL" .git)
    INTEGRATION_NAME="${REPO_NAME#integrify-}"       # Remove prefix
    INTEGRATION_NAME="${INTEGRATION_NAME%-python}"   # Remove suffix

    echo "📦 Fetching $REPO_NAME from $REPO_URL"

    git clone --depth 1 "$REPO_URL" "$TEMP_DIR/$REPO_NAME"

    # Copy source code (language-independent)
    SRC_PATH="$TEMP_DIR/$REPO_NAME/src/integrify/"
    if [ -d "$SRC_PATH" ]; then
        cp -r "$SRC_PATH" "$DEST_SRC"
        echo "  ✓ Copied source code"
    else
        echo "  ⚠️  No source code found at $SRC_PATH"
    fi

    # Copy documentation and partials for each language
    for LANG in "${LANGUAGES[@]}"; do
        LANG_DIR="$TEMP_DIR/$REPO_NAME/docs/$LANG"

        if [ ! -d "$LANG_DIR" ]; then
            echo "  ⚠️  Language '$LANG' not found, skipping"
            continue
        fi

        echo "  📄 Processing language: $LANG"

        # Copy documentation
        DOCS_PATH="$LANG_DIR/docs/integrations"
        DEST_DOCS="docs/$LANG/docs/integrations"

        if [ -d "$DOCS_PATH" ]; then
            mkdir -p "$DEST_DOCS"
            cp -r "$DOCS_PATH" "$DEST_DOCS/../"
            echo "    ✓ Copied $LANG documentation"
        else
            echo "    ⚠️  No documentation found at $DOCS_PATH"
        fi

        # Copy partials
        PARTIALS_PATH="$LANG_DIR/partial.yml"
        DEST_PARTIALS="docs/navs/$INTEGRATION_NAME.yml"

        if [ -f "$PARTIALS_PATH" ]; then
            mkdir -p "docs/$LANG/navs"
            cp "$PARTIALS_PATH" "$DEST_PARTIALS"
            echo "    ✓ Copied $LANG partials"
        else
            echo "    ⚠️  No partial.yml found at $PARTIALS_PATH"
        fi
    done

    echo "✅ Done with $REPO_NAME"
    echo ""
done < "$REPO_LIST_FILE"

# Clean up temp files
rm -rf "$TEMP_DIR"
echo "🎉 All integrations fetched and updated successfully."