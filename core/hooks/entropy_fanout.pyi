from _typeshed import Incomplete
from collections import Counter
from pathlib import Path

PAIRED: Incomplete

def fanout_counts(files: list) -> Counter: ...
def fanout_signals(files: list, root: Path, limit: int = ...) -> list: ...
