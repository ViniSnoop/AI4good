from _typeshed import Incomplete
from pathlib import Path

WORKSPACE_ROOT: Incomplete
SCHEMA: Incomplete
HARNESS_MANDATED: Incomplete
TRANSIENT_HEADING: str
TYPE_ROW: Incomplete
BACKTICKED_MD: Incomplete
UPPERCASE_MD: Incomplete
ROUTING_START: str
TREE_GLYPH: Incomplete
PATH_BULLET: Incomplete
INVENTORY_HEADING: Incomplete

def load_law(schema_path: Path) -> tuple[set, set]: ...
def check_name(path: Path, allowed: set, exempt: set) -> str | None: ...
def check_inventory(path: Path) -> str | None: ...
def staged_added_files() -> list: ...
def main() -> int: ...
