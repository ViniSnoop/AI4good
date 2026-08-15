from _typeshed import Incomplete
from pathlib import Path

SCANNED: Incomplete
SKIP_DIRS: Incomplete

def tracked_files(root: Path, nested: bool = False) -> list: ...
def nested_repos(root: Path, depth: int = 3) -> list: ...

ENFORCEMENT: Incomplete

def enforcement_paths(root: Path) -> set: ...

MEMORY_DIR: str

def wiki_exempt_paths(root: Path) -> set: ...
