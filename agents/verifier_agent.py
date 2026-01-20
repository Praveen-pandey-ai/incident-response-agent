class VerifierAgent:
    """
    Validates that all claims are evidence-backed.
    """

    def run(self, triage_result, timeline, hypotheses):
        validated_hypotheses = []
        rejected = []

        for h in hypotheses:
            if h.get("evidence"):
                validated_hypotheses.append(h)
            else:
                rejected.append({
                    "hypothesis": h["hypothesis"],
                    "reason": "No supporting evidence"
                })

        final_root_cause = None
        if validated_hypotheses:
            final_root_cause = validated_hypotheses[0]
        else:
            final_root_cause = "Inconclusive"

        return {
            "severity": triage_result["severity"],
            "impacted_services": triage_result["impacted_services"],
            "start_time": triage_result["start_time"],
            "timeline": timeline,
            "root_cause": final_root_cause,
            "rejected_hypotheses": rejected
        }
