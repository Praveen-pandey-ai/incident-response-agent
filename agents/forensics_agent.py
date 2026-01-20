from tools.log_search import log_search


class ForensicsAgent:
    """
    Investigates logs and builds an evidence-backed timeline.
    """

    def run(self, log_paths, start_time):
        timeline = []

        for service, path in log_paths.items():
            results = log_search(
                log_path=path,
                pattern="ERROR|WARN",
                start_time=start_time
            )

            for r in results:
                timeline.append({
                    "service": service,
                    "timestamp": r["timestamp"],
                    "event": r["content"],
                    "evidence": f"{path}:L{r['line_number']}"
                })

        # Sort timeline chronologically
        timeline.sort(key=lambda x: x["timestamp"])

        return timeline
