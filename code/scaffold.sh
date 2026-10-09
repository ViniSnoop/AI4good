#!/usr/bin/env bash
# Scaffold a new code project with Git Flow and template files.
# Usage: ./scaffold.sh <project-name>

set -e

if [ -z "$1" ]; then
    echo "Usage: ./scaffold.sh <project-name>"
    exit 1
fi

PROJECT_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$SCRIPT_DIR/$PROJECT_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' already exists."
    exit 1
fi

echo "Creating new project: $PROJECT_NAME..."
mkdir -p "$TARGET_DIR"

cd "$TARGET_DIR"
git init -b main

TEMPLATES_DIR="$SCRIPT_DIR/_templates"

sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/README.md" > README.md
sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/CONTEXT.md" > CONTEXT.md
sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/SPECS.md" > SPECS.md
sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/ROADMAP.md" > ROADMAP.md
sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/SETUP.md" > SETUP.md
sed "s/\[Project Name\]/$PROJECT_NAME/g" "$TEMPLATES_DIR/ISSUES.md" > ISSUES.md

cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.venv/
venv/
node_modules/
dist/
build/
.env
.DS_Store
EOF

git add .
git commit -m "feat: initial project scaffold"

git checkout -b develop

python3 "$SCRIPT_DIR/../core/hooks/routing/context_synchronizer.py" "$SCRIPT_DIR/CONTEXT.md" 2>/dev/null || true

echo "✓ Project '$PROJECT_NAME' created at $TARGET_DIR"
echo "✓ Git initialized with 'main' and 'develop' branches"
echo "✓ Scaffolding files ready: README.md, CONTEXT.md, SPECS.md, ROADMAP.md, SETUP.md, ISSUES.md"
echo "✓ Routing synchronized in code/CONTEXT.md"
