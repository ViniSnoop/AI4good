from _typeshed import Incomplete
from entropy_corpus import enforcement_paths as enforcement_paths
from pathlib import Path

HARNESS_MANDATED: Incomplete
UPPERCASE_MD: Incomplete

def check_name(path: Path, allowed: set, exempt: set) -> str | None: ...
def failures_for(path: Path, allowed: set, exempt: set, scopes: dict, vocabulary: set) -> list: ...
def main() -> int: ...
