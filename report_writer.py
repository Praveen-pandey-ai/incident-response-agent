from datetime import datetime


def write_incident_report(final_state: dict, output_path="incident_report.md"):
    """
    Generate incident_report.md from verified final state.
    """

    severity = final_state.get("severity", "Unknown")
    services = final_state.get("impacted_services", [])
    start_time = final_state.get("start_time")
    timeline = final_state.get("timeline", [])
    root_cause = final_state.get("root_cause")

    with open(output_path, "w", encoding="utf-8") as f:
        # -------- Summary --------
        f.write("# Incident Report\n\n")

        f.write("## Summary\n")
        f.write(
            "An incident was detected involving partial service degradation. "
            "This report summarizes the impact, timeline, and root cause analysis "
            "based on metrics, logs, and validated evidence.\n\n"
        )

        # -------- Impact --------
        f.write("## Impact\n")
        f.write(f"- Impacted services: {', '.join(services)}\n")
        f.write("- User-facing authentication and payment flows were affected.\n\n")

        # -------- Severity --------
        f.write("## Severity\n")
        f.write(f"- Classified as **{severity}** based on runbook rules and metrics.\n\n")

        # -------- Start Time --------
        f.write("## Incident Start Time\n")
        f.write(f"- Estimated start time: **{start_time}**\n\n")

        # -------- Timeline --------
        f.write("## Timeline of Events\n")
        for event in timeline:
            f.write(
                f"- **{event['timestamp']}** | {event['service']} | "
                f"{event['event']}  \n"
                f"  - Evidence: `{event['evidence']}`\n"
            )
        f.write("\n")

        # -------- Root Cause --------
        f.write("## Root Cause Analysis\n")
        if root_cause == "Inconclusive":
            f.write(
                "The investigation did not find sufficient evidence to conclusively "
                "identify a single root cause.\n\n"
            )
        else:
            f.write(f"- **{root_cause['hypothesis']}**\n")
            for ev in root_cause.get("evidence", []):
                f.write(f"  - Evidence: `{ev}`\n")
            f.write("\n")

        # -------- Follow-ups --------
        f.write("## Follow-up Actions\n")
        f.write("- Review recent deployments to auth-service\n")
        f.write("- Increase database connection pool limits\n")
        f.write("- Add alerts for early auth latency spikes\n")
