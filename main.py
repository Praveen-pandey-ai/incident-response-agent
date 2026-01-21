from state.graph import build_incident_graph
from report_writer import write_incident_report
from action_items_writer import write_action_items


def main():
    """
    Entry point for the Agentic Incident Response system.
    Runs the LangGraph workflow and generates outputs.
    """

    # 1. Build the LangGraph state machine
    graph = build_incident_graph()

    # 2. Initial empty state (LangGraph will populate it)
    initial_state = {}

    # 3. Execute the graph
    final_state = graph.invoke(initial_state)

    # 4. Extract verifier-approved final result
    final_result = final_state.get("final", {})

    # 5. Print a concise console summary (for evaluator visibility)
    print("\n=== INCIDENT ANALYSIS RESULT ===\n")
    print(f"Severity           : {final_result.get('severity')}")
    print(f"Impacted Services  : {final_result.get('impacted_services')}")
    print(f"Incident Start     : {final_result.get('start_time')}\n")

    print("Root Cause:")
    print(final_result.get("root_cause"))
    print("\nTimeline:")

    for event in final_result.get("timeline", []):
        print(
            f"- [{event['timestamp']}] "
            f"{event['service']} | {event['event']} "
            f"({event['evidence']})"
        )

    # 6. Generate incident_report.md (required deliverable)
    write_incident_report(final_result)

    print("\n✔ incident_report.md generated successfully\n")

    write_action_items(final_result)

    print("✔ action_items.json generated successfully\n")


    


if __name__ == "__main__":
    main()
