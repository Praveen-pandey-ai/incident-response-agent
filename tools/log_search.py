import re
from datetime import datetime
from pathlib import Path


def log_search(
    log_path: str,
    pattern: str,
    start_time: datetime | None = None,
    end_time: datetime | None = None
):
    """
    Search a log file for lines matching a regex pattern and optional time range.
    Returns matched lines with line numbers and timestamps.
    """
    results = []

    path = Path(log_path)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    regex = re.compile(pattern)

    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            # Extract timestamp (first token)
            try:
                ts_str = line.split(" ")[0]
                timestamp = datetime.fromisoformat(
                    ts_str.replace("Z", "+00:00")
                )
            except Exception:
                # Skip malformed lines
                continue

            # Time window filter
            if start_time and timestamp < start_time:
                continue
            if end_time and timestamp > end_time:
                continue

            # Pattern match
            if regex.search(line):
                results.append({
                    "line_number": line_no,
                    "timestamp": timestamp,
                    "content": line
                })

    return results
