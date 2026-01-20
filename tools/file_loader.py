import json
import csv
from pathlib import Path

ALLOWED_EXTENSIONS = {".json", ".csv", ".txt", ".md", ".log"}


def load_file(path: str):
    """
    Safely load a file based on extension.
    Returns structured data or raw text.
    """
    file_path = Path(path)

    if file_path.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type not allowed: {file_path.suffix}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if file_path.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    if file_path.suffix == ".csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # txt, md, log
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
