# GitHub Repository Setup

## Create Repository

1. Go to https://github.com/new
2. Repository name: `AI4good-workspace` (or your preferred name)
3. Description: "Workspace for Advanced AI Topics course - code and papers"
4. **Public** or **Private** (your choice)
5. **DO NOT** initialize with:
   - README
   - .gitignore
   - License
6. Click "Create repository"

## Connect Local Repository

```bash
cd /home/vini/Downloads/AI4good/workspace

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AI4good-workspace.git

# Push main branch
git branch -M main
git push -u origin main

# Create and push develop branch
git checkout -b develop
git push -u origin develop

# Return to main
git checkout main
```

## Configure Branch Protection (Required for Git Flow)

### For `main` branch:
1. Go to Settings → Branches
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
   - ✅ Do not allow bypassing the above settings
5. Click "Create"

### For `develop` branch:
1. Click "Add branch protection rule" again
2. Branch name pattern: `develop`
3. Enable same settings as above
4. Click "Create"

## GitHub CLI Authentication (Optional but Recommended)

```bash
# Install gh if not present
# Then authenticate:
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
# Paste the code shown and authorize

# Verify
gh auth status

# Set up git credential helper
gh auth setup-git
```

## Verify Setup

```bash
# Check remotes
git remote -v

# Check branches
git branch -a

# Test push (dry run)
git push --dry-run origin HEAD
```