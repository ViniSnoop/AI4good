# Overleaf Sync Setup

## Option 1: Create New Overleaf Project

1. Go to https://overleaf.com and create a new project
2. Choose "Blank Project" or a template (e.g., "IEEE Conference")
3. Note the project URL: `https://www.overleaf.com/project/<PROJECT_ID>`
4. The git URL will be: `https://git.overleaf.com/<PROJECT_ID>`

## Option 2: Use Existing Overleaf Project

1. Open your project on Overleaf
2. Click "Menu" → "Git" → Copy the git URL
3. Format: `https://git.overleaf.com/<PROJECT_ID>`

## Connect Local Papers Folder

```bash
cd /home/vini/Downloads/AI4good/workspace/papers

# If starting fresh, initialize git
git init

# Add Overleaf as remote
git remote add overleaf https://git.overleaf.com/<PROJECT_ID>

# Pull existing content (if any)
git pull overleaf main --allow-unrelated-histories

# Or push local content to Overleaf
git add .
git commit -m "Initial commit: paper structure"
git push -u overleaf main
```

## Sync Workflow

### Local → Overleaf (after writing)
```bash
cd /home/vini/Downloads/AI4good/workspace/papers/<paper-name>
# Compile locally first to verify
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex

# Commit and push
git add .
git commit -m "Update paper: <description>"
git push overleaf main
```

### Overleaf → Local (after co-author edits)
```bash
cd /home/vini/Downloads/AI4good/workspace/papers/<paper-name>
git pull overleaf main
# Recompile to verify
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
```

## Multiple Papers

Each paper should be its own folder under `papers/` with its own git repo:

```
papers/
├── paper-1/
│   ├── main.tex
│   ├── refs/
│   └── .git/ (connected to Overleaf project 1)
├── paper-2/
│   ├── main.tex
│   ├── refs/
│   └── .git/ (connected to Overleaf project 2)
```

## Authentication

Overleaf git uses your Overleaf account credentials:
- Username: your Overleaf email
- Password: your Overleaf password (or API token)

For API token (recommended):
1. Go to Overleaf Account Settings → API Tokens
2. Generate a token
3. Use token as password when prompted

## Tips

- **Always compile locally first** before pushing to Overleaf
- Use `latexmk -C` for clean rebuild
- Keep `.gitignore` for build artifacts (*.aux, *.log, *.out, *.pdf, etc.)
- Overleaf is the collaboration sync point; local is authoritative for compilation