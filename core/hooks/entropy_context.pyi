from _typeshed import Incomplete
from pathlib import Path

ROUTING_START: str
TREE_GLYPH: Incomplete
PATH_BULLET: Incomplete
INVENTORY_HEADING: Incomplete
GOAL_LINE: Incomplete

def check_inventory(path: Path) -> str | None: ...
def is_project(path: Path) -> bool: ...
def check_goal_link(path: Path) -> str | None: ...
