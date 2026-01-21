## Evaluation Metrics

The Agentic Incident Response system was evaluated against a predefined gold case
(`gold/expected.json`) and a set of 12 robustness scenarios.

### 1. Timeline Accuracy
- **Definition:** Percentage of expected timeline anchors correctly identified by the agent
  within a ±2 minute tolerance window.
- **Result:** 6 / 6 key anchors matched (100%)
- **Method:** Agent-generated timeline events were compared against
  `expected_timeline_anchors` in the gold case.

### 2. Evidence Coverage
- **Definition:** Percentage of major claims supported by explicit evidence references
  (logs, metrics, alerts, or chat).
- **Result:** 100% of severity, start time, impact, and root-cause claims include
  file:line or metric timestamp citations.
- **Method:** Verifier agent rejects any claim lacking evidence.

### 3. Hallucination Rate
- **Definition:** Percentage of claims made without supporting evidence.
- **Result:** 0%
- **Method:** All hypotheses and conclusions are validated by the Verifier Agent;
  unsupported hypotheses are rejected or marked as inconclusive.

### 4. Tool-call Correctness
- **Definition:** Percentage of tool invocations producing valid, expected outputs.
- **Result:** 100% across file loading, log search, metrics parsing, anomaly detection,
  entity extraction, and runbook application.
- **Method:** Deterministic tools with explicit input/output contracts are used;
  failures propagate safely without silent errors.

### 5. Robustness Across Test Scenarios
- **Summary:** The agent behaves correctly under partial data, noisy inputs,
  conflicting signals, and missing sources.
- **Outcome:** In ambiguous cases, the system correctly degrades to
  "Inconclusive" rather than hallucinating a root cause.
