def detect_anomalies(
    metrics_by_service,
    latency_multiplier=2.5,
    error_rate_multiplier=3.0
):
    """
    Detect simple anomalies in latency and error rate using baseline comparison.

    Returns a list of detected anomalies with evidence-ready details.
    """
    anomalies = []

    for service, points in metrics_by_service.items():
        if len(points) < 3:
            # Not enough data to establish baseline
            continue

        # Use first half as baseline
        baseline_points = points[: len(points) // 2]

        baseline_latency = sum(p["latency_ms"] for p in baseline_points) / len(baseline_points)
        baseline_error = sum(p["error_rate"] for p in baseline_points) / len(baseline_points)

        for p in points[len(points) // 2:]:
            if p["latency_ms"] > baseline_latency * latency_multiplier:
                anomalies.append({
                    "service": service,
                    "timestamp": p["timestamp"],
                    "metric": "latency_ms",
                    "value": p["latency_ms"],
                    "baseline": baseline_latency
                })

            if p["error_rate"] > baseline_error * error_rate_multiplier:
                anomalies.append({
                    "service": service,
                    "timestamp": p["timestamp"],
                    "metric": "error_rate",
                    "value": p["error_rate"],
                    "baseline": baseline_error
                })

    return anomalies
