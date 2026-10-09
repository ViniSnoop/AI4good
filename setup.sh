#!/bin/bash
# AI4good Workspace Setup Script
# Run this after cloning the repository

set -e

WORKSPACE_ROOT="/home/vini/Downloads/AI4good/workspace"

echo "=== AI4good Workspace Setup ==="
echo "Workspace root: $WORKSPACE_ROOT"
cd "$WORKSPACE_ROOT"

# 1. Check/Install Python venv
echo "--- Setting up Python venv ---"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created .venv"
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install mypy

# 2. Check/Install Node.js and TypeScript
echo "--- Checking Node.js ---"
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Installing via nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install --lts
fi
if ! command -v tsc &> /dev/null; then
    npm install -g typescript
fi

# 3. Check/Install LaTeX (requires sudo - run manually)
echo "--- LaTeX Toolchain ---"
echo "Run manually with sudo:"
echo "  sudo apt-get update"
echo "  sudo apt-get install -y latexmk texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra"
echo "  # For Times New Roman:"
echo "  printf 'ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true\n' | sudo debconf-set-selections"
echo "  sudo apt-get install -y ttf-mscorefonts-installer"

# 4. Check/Install RTK
echo "--- Checking RTK ---"
if ! command -v rtk &> /dev/null; then
    echo "Installing RTK..."
    curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
fi

# 5. Check/Install ddgr for web search
echo "--- Checking ddgr ---"
if ! command -v ddgr &> /dev/null; then
    echo "Installing ddgr..."
    sudo apt-get install -y ddgr  # or: pipx install ddgr
fi

# 6. Git hooks
echo "--- Setting up Git hooks ---"
git config --global core.hooksPath "$WORKSPACE_ROOT/core/hooks"
chmod +x core/hooks/post-edit.sh core/hooks/read/pre-read.sh core/hooks/pre-commit \
         core/hooks/checks/check-line-counts.sh core/hooks/copilot/copilot-agent.sh \
         core/hooks/session/start-session.sh core/tools/wos/deps

# 7. Caveman setup
echo "--- Setting up Caveman ---"
core/tools/wos/sync-global-skills
mkdir -p ~/.config/caveman
echo '{"defaultMode": "full"}' > ~/.config/caveman/config.json
if ! grep -q "caveman-compress()" ~/.bashrc; then
    cat >> ~/.bashrc << 'CAVEMAN_EOF'

# caveman-compress shortcut
caveman-compress() {
  local CLAUDE_BIN
  CLAUDE_BIN="$(dirname "$CLAUDE_CODE_EXECPATH")"
  (cd "$WORKSPACE_ROOT/core/skills/caveman" && PATH="$CLAUDE_BIN:$PATH" python3 -m scripts "$1")
}
CAVEMAN_EOF
    source ~/.bashrc
fi

# 8. Verify installation
echo "--- Verification ---"
core/tools/wos/deps --check
git config --global core.hooksPath
.venv/bin/stubgen --version && tsc --version
node --input-type=module -e "import('$WORKSPACE_ROOT/.opencode/plugins/workspace-policy.js').then(m=>console.log(typeof m.WorkspacePolicy))"
make verify-fast

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Create GitHub repo and add remote (see GITHUB_SETUP.md)"
echo "2. Run LaTeX installation commands (shown above)"
echo "3. Configure Overleaf sync (see OVERLEAF_SETUP.md)"
echo "4. Open workspace in opencode: opencode"