#!/bin/bash
set -e

REPO_LIST_FILE="integrations.txt"
TEMP_DIR="integrations-tmp"

if [ ! -f "$REPO_LIST_FILE" ]; then
    echo "❌ $REPO_LIST_FILE not found!"
    exit 1
fi

# Clean temp and output dirs
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

DEST_SRC="src/"
rm -rf "$DEST_SRC"/integrify/*
DEST_DOCS="docs/az/docs/"
rm -rf "$DEST_DOCS"/integrations/*

echo "🔄 Starting to fetch integrations..."

while IFS= read -r REPO_URL; do
    [ -z "$REPO_URL" ] && continue  # Skip empty lines

    REPO_NAME=$(basename "$REPO_URL" .git)
    INTEGRATION_NAME="${REPO_NAME#integrify-}"       # Remove prefix
    INTEGRATION_NAME="${INTEGRATION_NAME%-python}"   # Remove suffix

    echo "📦 Fetching $REPO_NAME from $REPO_URL"

    git clone --depth 1 "$REPO_URL" "$TEMP_DIR/$REPO_NAME"

    # Copy source code
    SRC_PATH="$TEMP_DIR/$REPO_NAME/src/integrify/"
    cp -r "$SRC_PATH" "$DEST_SRC"

    # Copy documentation
    DOCS_PATH="$TEMP_DIR/$REPO_NAME/docs/az/docs/integrations"
    cp -r "$DOCS_PATH" "$DEST_DOCS"

    # Copy partials
    PARTIALS_PATH="$TEMP_DIR/$REPO_NAME/docs/az/partial.yml"
    DEST_PARTIALS="docs/az/navs/$INTEGRATION_NAME.yml"
    cp "$PARTIALS_PATH" "$DEST_PARTIALS"

    echo "✅ Done with $REPO_NAME"
    echo ""
done < "$REPO_LIST_FILE"

# Clean up temp files
rm -rf "$TEMP_DIR"
echo "🎉 All integrations fetched and updated successfully."
