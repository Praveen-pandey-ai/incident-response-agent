from tools.entity_extractor import extract_entities
from tools.runbook_engine import apply_runbook


class TriageAgent:
    """
    Determines impacted services, severity, and rough start time.
    """

    def run(self, alerts, anomalies, chat_text):
        impacted_services = set()
        reasons = []

        # --- Extract services from alerts ---
        for alert in alerts:
            impacted_services.add(alert["service"])
            reasons.append(
                f"Alert reported for {alert['service']} at {alert['timestamp']}"
            )

        # --- Extract services from chat ---
        chat_entities = extract_entities(chat_text)
        for svc in chat_entities["services"]:
            impacted_services.add(svc)
            reasons.append(
                f"Service {svc} mentioned in incident chat"
            )

        # --- Estimate start time from anomalies ---
        start_time = None
        if anomalies:
            start_time = min(a["timestamp"] for a in anomalies)
            reasons.append(
                f"Earliest anomaly detected at {start_time}"
            )

        # --- Apply runbook ---
        runbook_result = apply_runbook(
            impacted_services=list(impacted_services),
            anomalies=anomalies,
            extracted_entities=chat_entities
        )

        return {
            "impacted_services": list(impacted_services),
            "severity": runbook_result["severity"],
            "start_time": start_time,
            "escalations": runbook_result["escalations"],
            "reasons": reasons + runbook_result["reasons"]
        }
