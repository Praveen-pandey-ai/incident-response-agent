from state.graph import build_incident_graph

# Build and run investigation graph
graph = build_incident_graph()
final_state = graph.invoke({})
final_result = final_state.get("final", {})

# Access results
print("\n=== INCIDENT ANALYSIS RESULT ===\n")
print(f"Severity: {final_result.get('severity')}")
print(f"Impacted Services: {final_result.get('impacted_services')}")
print(f"Start Time: {final_result.get('start_time')}\n")
print(f"Root Cause:\n{final_result.get('root_cause')}\n")
print("Timeline:")
for event in final_result.get("timeline", []):
    print(f"- [{event['timestamp']}] {event['service']} | {event['event']}")