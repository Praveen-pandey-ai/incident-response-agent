# Incident Response Agent — Test Scenarios

This document defines robustness tests for the Agentic Incident Response system.

---

## Test 1: Baseline (Gold Case)
**Condition:** All inputs present and consistent  
**Expected:**  
- Severity: SEV-2  
- Root cause correctly identified  
- Timeline matches gold anchors  

---

## Test 2: Partial Logs Missing
**Condition:** `payments.log` unavailable  
**Expected:**  
- Payments marked as impacted via alerts/metrics  
- Root cause still attributed to auth-service  
- Confidence reduced but not inconclusive  

---

## Test 3: Noisy Chat
**Condition:** Chat contains irrelevant discussion and speculation  
**Expected:**  
- Chat clues validated against logs/metrics  
- Unsupported chat hypotheses rejected  

---

## Test 4: Conflicting Alerts
**Condition:** Alerts show SEV-3 while metrics show severe degradation  
**Expected:**  
- Severity derived from metrics + runbook  
- Alert severity overridden  

---

## Test 5: Metrics Spike Without Logs
**Condition:** Metrics show spike but logs show no ERROR entries  
**Expected:**  
- Incident detected  
- Root cause marked as "Inconclusive"  

---

## Test 6: Logs Without Metrics
**Condition:** Metrics missing but logs show repeated ERRORs  
**Expected:**  
- Incident detected via logs  
- Start time inferred from logs  

---

## Test 7: Unrelated Service Noise
**Condition:** Orders-service logs show WARN-level noise  
**Expected:**  
- Orders not treated as root cause  
- Severity remains SEV-2  

---

## Test 8: Runbook Contradiction
**Condition:** Runbook suggests SEV-3 but impact is severe  
**Expected:**  
- Agent prioritizes metrics/logs  
- Severity escalated appropriately  

---

## Test 9: Human Declares Wrong Severity
**Condition:** Chat declares SEV-1 without evidence  
**Expected:**  
- Severity determined independently  
- Chat claim ignored  

---

## Test 10: Multiple Possible Root Causes
**Condition:** Auth and payments both show ERRORs  
**Expected:**  
- Multiple hypotheses generated  
- Ranked by evidence strength  

---

## Test 11: Missing Chat Input
**Condition:** `chat.txt` unavailable  
**Expected:**  
- Incident analysis proceeds  
- No reliance on human input  

---

## Test 12: Clean Recovery Signals
**Condition:** Metrics return to baseline mid-incident  
**Expected:**  
- Timeline shows recovery  
- Incident still reported with correct start time  

---
