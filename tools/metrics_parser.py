from collections import defaultdict
from datetime import datetime


def parse_metrics(rows):
    """
    Convert CSV rows into a time-series structure grouped by service.
    """
    metrics_by_service = defaultdict(list)

    for row in rows:
        try:
            metrics_by_service[row["service"]].append({
                "timestamp": datetime.fromisoformat(
                    row["timestamp"].replace("Z", "+00:00")
                ),
                "latency_ms": float(row["latency_ms"]),
                "error_rate": float(row["error_rate"])
            })
        except Exception as e:
            # Skip malformed rows safely
            continue

    # Ensure time ordering
    for service in metrics_by_service:
        metrics_by_service[service].sort(key=lambda x: x["timestamp"])

    return dict(metrics_by_service)
