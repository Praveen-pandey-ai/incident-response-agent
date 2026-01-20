def write_action_items(final_state: dict, output_path="action_items.json"):
    """
    Generate action_items.json from verified final incident state.
    """

    action_items = []

    root_cause = final_state.get("root_cause")
    impacted_services = final_state.get("impacted_services", [])

    # --- Root cause–driven actions ---
    if isinstance(root_cause, dict):
        hypothesis = root_cause.get("hypothesis", "").lower()

        if "database connection pool" in hypothesis:
            action_items.append({
                "task": "Increase database connection pool limits for auth-service",
                "priority": "high",
                "owner": "database-team"
            })

            action_items.append({
                "task": "Review recent auth-service deployment for connection leaks",
                "priority": "high",
                "owner": "auth-team"
            })

    # --- Preventive actions ---
    if "auth-service" in impacted_services:
        action_items.append({
            "task": "Add early-warning alerts for auth-service latency spikes",
            "priority": "medium",
            "owner": "auth-team"
        })

    if "payments-service" in impacted_services:
        action_items.append({
            "task": "Improve resilience of payments-service against auth-service timeouts",
            "priority": "medium",
            "owner": "payments-team"
        })

    # --- Fallback if no clear root cause ---
    if not action_items:
        action_items.append({
            "task": "Perform deeper investigation to identify root cause",
            "priority": "medium",
            "owner": "unknown"
        })

    # --- Write file ---
    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(action_items, f, indent=2)
