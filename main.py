from state.graph import build_incident_graph


def main():
    """
    Entry point for the Agentic Incident Response system.
    """
    graph = build_incident_graph()

    # Initial empty state (LangGraph will populate it)
    initial_state = {}

    # Run the graph
    final_state = graph.invoke(initial_state)

    # For now, just display the final validated output
    final_result = final_state.get("final", {})

    print("\n=== INCIDENT ANALYSIS RESULT ===\n")
    print(f"Severity: {final_result.get('severity')}")
    print(f"Impacted Services: {final_result.get('impacted_services')}")
    print(f"Start Time: {final_result.get('start_time')}")
    print("\nRoot Cause:")
    print(final_result.get("root_cause"))

    print("\nTimeline Events:")
    for event in final_result.get("timeline", []):
        print(
            f"- [{event['timestamp']}] "
            f"{event['service']} | {event['event']} "
            f"({event['evidence']})"
        )


if __name__ == "__main__":
    main()
