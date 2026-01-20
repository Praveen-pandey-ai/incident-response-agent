from tools.entity_extractor import extract_entities


class HypothesisAgent:
    """
    Generates and ranks root cause hypotheses.
    """

    def run(self, timeline):
        hypotheses = []

        # Hypothesis 1: DB connection exhaustion in auth
        auth_events = [
            e for e in timeline
            if "auth-service" in e["service"]
            and "exhausted" in e["event"].lower()
        ]

        if auth_events:
            hypotheses.append({
                "hypothesis": "Auth-service database connection pool exhaustion",
                "confidence": "high",
                "evidence": [e["evidence"] for e in auth_events]
            })

        # Hypothesis 2: Cascading failure to payments
        payment_events = [
            e for e in timeline
            if "payments-service" in e["service"]
            and "auth" in e["event"].lower()
        ]

        if payment_events:
            hypotheses.append({
                "hypothesis": "Payments failures due to upstream auth-service issues",
                "confidence": "medium",
                "evidence": [e["evidence"] for e in payment_events]
            })

        return hypotheses
