def apply_runbook(
    impacted_services,
    anomalies,
    extracted_entities
):
    """
    Apply runbook rules to determine severity and escalation targets.
    Returns a structured decision with reasoning.
    """

    severity = "SEV-3"
    escalations = set()
    reasons = []

    # --- Severity rules ---
    for anomaly in anomalies:
        if (
            anomaly["service"] == "auth-service"
            and anomaly["metric"] == "error_rate"
            and anomaly["value"] >= 0.05
        ):
            severity = "SEV-2"
            reasons.append(
                "Auth-service error rate exceeded 5% based on metrics"
            )

    if len(impacted_services) >= 3:
        severity = "SEV-1"
        reasons.append(
            "Multiple critical services impacted"
        )

    # --- Escalation rules ---
    if "auth-service" in impacted_services:
        escalations.add("auth-team")
        reasons.append(
            "Auth-service identified as impacted service"
        )

    if "database-team" in extracted_entities.get("owners", []):
        escalations.add("database-team")
        reasons.append(
            "Database-related issues detected in logs or chat"
        )

    return {
        "severity": severity,
        "escalations": list(escalations),
        "reasons": reasons
    }
