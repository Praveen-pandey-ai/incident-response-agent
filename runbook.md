# Incident Response Runbook

## Severity Levels

**SEV-1**
- Complete service outage
- All users impacted
- No workaround available

**SEV-2**
- Partial service outage or severe degradation
- Significant user impact
- Core functionality affected but system partially operational

**SEV-3**
- Minor degradation
- Limited user impact
- Workarounds available

---

## Escalation Rules

- If authentication failures exceed 5% for more than 5 minutes, escalate to Auth Team.
- If payment failures are caused by upstream dependency issues, do not escalate to Payments Team immediately.
- Database-related issues should involve the Database Team after confirmation via logs or metrics.

---

## Investigation Checklist

1. Check recent deployments.
2. Review service logs for ERROR patterns.
3. Correlate metric anomalies with log timestamps.
4. Validate human-reported issues with system data.

---

## Notes

- Human reports may be incomplete or inaccurate.
- Always prioritize metrics and logs over chat messages.
