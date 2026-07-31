#!/usr/bin/env python3
# PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description.
import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from file_law import CODE_EXTS, is_code_file, is_vendored, load_limits
from hook_input import parse_stdin

CONTENT_EXTS = {'.md', '.yaml', '.yml', '.toml'}
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]

_limits = load_limits()
WARN_LINES, BLOCK_LINES = _limits['WARN_LINES'], _limits['BLOCK_LINES']

FIRST_LINE_COMMENT = {
	'.py': r'^\s*#',    '.js':   r'^\s*//', '.ts':   r'^\s*//',
	'.tsx': r'^\s*//', '.dart': r'^\s*//', '.css':  r'^\s*/\*',
	'.scss': r'^\s*/\*', '.html': r'^\s*<!--',
	'.yaml': r'^\s*#', '.yml':  r'^\s*#', '.toml': r'^\s*#',
	'.tex': r'^\s*%',  '.md':   r'^\s*(#|---\s*$)',  # md: title or YAML frontmatter (skills)
}

EXAMPLE_COMMENT = {
	'.py': '# Short description',   '.js':   '// Short description',
	'.ts': '// Short description',  '.tsx':  '// Short description',
	'.dart': '// Short description', '.css': '/* Short description */',
	'.scss': '/* Short description */', '.html': '<!-- Short description -->',
	'.yaml': '# Short description', '.yml':  '# Short description',
	'.toml': '# Short description', '.tex': '% Short description of this section',
	'.md': '# Title of this document',
}

_, tool, data, _, _ = parse_stdin()
file_path = data.get('file_path', '')
basename  = os.path.basename(file_path)

# CONTEXT.md: new files must have a description on line 2 (> short description)
if basename == 'CONTEXT.md' and tool == 'Write' and not os.path.exists(file_path):
	lines = data.get('content', '').splitlines()
	line2 = lines[1].strip() if len(lines) > 1 else ''
	if not re.match(r'^>\s*\S', line2):
		print(f"⛔ CONTEXT.md DESCRIPTION MISSING — {file_path}")
		print(f"   Line 2 must be: > Short description of this directory")
		sys.exit(2)

_, ext = os.path.splitext(file_path)
_path      = Path(file_path)
is_code    = is_code_file(_path) and not is_vendored(_path, WORKSPACE_ROOT)
is_content = ext in CONTENT_EXTS and basename != 'CONTEXT.md'

if not is_code and not is_content:
	sys.exit(0)

if tool == 'Write':
	content   = data.get('content', '')
	new_lines = len(content.splitlines())
	if not os.path.exists(file_path):
		pattern = FIRST_LINE_COMMENT.get(ext)
		first   = content.splitlines()[0] if content.strip() else ''
		if pattern and not re.match(pattern, first):
			print(f"⛔ FIRST-LINE MISSING — {file_path}")
			print(f"   New files must start with a description.")
			print(f"   Example: {EXAMPLE_COMMENT.get(ext, '# Description')}")
			sys.exit(2)

elif tool == 'Edit':
	if not os.path.exists(file_path):
		sys.exit(0)
	current_lines = len(open(file_path).read().splitlines())
	net       = data.get('new_string', '').count('\n') - data.get('old_string', '').count('\n')
	new_lines = current_lines + net

else:
	sys.exit(0)

if is_code and new_lines >= BLOCK_LINES:
	print(f"⛔ SIZE GATE — {file_path} would reach {new_lines} lines (limit: {BLOCK_LINES}).")
	print(f"   Extract shared logic into a new module and import it from existing callers.")
	print(f"   Do NOT copy existing functions into a new file — copies are blocked at commit.")
	sys.exit(2)

sys.exit(0)
