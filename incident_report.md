# Incident Report

## Summary
An incident was detected involving partial service degradation. This report summarizes the impact, timeline, and root cause analysis based on metrics, logs, and validated evidence.

## Impact
- Impacted services: auth-service, payments-service, orders-service
- User-facing authentication and payment flows were affected.

## Severity
- Classified as **SEV-1** based on runbook rules and metrics.

## Incident Start Time
- Estimated start time: **2026-01-17 10:41:00+00:00**

## Timeline of Events
- **2026-01-17 10:41:10+00:00** | auth-service | 2026-01-17T10:41:10Z ERROR Database connection pool exhausted  
  - Evidence: `logs/auth.log:L4`
- **2026-01-17 10:41:25+00:00** | auth-service | 2026-01-17T10:41:25Z ERROR Failed to acquire DB connection within timeout  
  - Evidence: `logs/auth.log:L5`
- **2026-01-17 10:42:05+00:00** | auth-service | 2026-01-17T10:42:05Z ERROR Login request failed due to DB timeout  
  - Evidence: `logs/auth.log:L6`
- **2026-01-17 10:43:05+00:00** | payments-service | 2026-01-17T10:43:05Z WARN Slow response from auth-service during token validation  
  - Evidence: `logs/payments.log:L3`
- **2026-01-17 10:43:20+00:00** | auth-service | 2026-01-17T10:43:20Z ERROR Login request failed due to DB timeout  
  - Evidence: `logs/auth.log:L7`
- **2026-01-17 10:44:10+00:00** | auth-service | 2026-01-17T10:44:10Z WARN Retrying database connection  
  - Evidence: `logs/auth.log:L8`
- **2026-01-17 10:44:15+00:00** | payments-service | 2026-01-17T10:44:15Z ERROR Payment request failed: auth-service timeout  
  - Evidence: `logs/payments.log:L4`
- **2026-01-17 10:44:40+00:00** | orders-service | 2026-01-17T10:44:40Z WARN Slight increase in order processing latency  
  - Evidence: `logs/orders.log:L3`
- **2026-01-17 10:45:00+00:00** | auth-service | 2026-01-17T10:45:00Z ERROR Database connection pool exhausted  
  - Evidence: `logs/auth.log:L9`
- **2026-01-17 10:45:10+00:00** | payments-service | 2026-01-17T10:45:10Z ERROR Payment request failed: unable to validate user token  
  - Evidence: `logs/payments.log:L5`
- **2026-01-17 10:46:30+00:00** | payments-service | 2026-01-17T10:46:30Z WARN Retrying payment after auth failure  
  - Evidence: `logs/payments.log:L6`
- **2026-01-17 10:47:20+00:00** | payments-service | 2026-01-17T10:47:20Z ERROR Payment request failed: auth-service unreachable  
  - Evidence: `logs/payments.log:L7`

## Root Cause Analysis
- **Auth-service database connection pool exhaustion**
  - Evidence: `logs/auth.log:L4`
  - Evidence: `logs/auth.log:L9`

## Follow-up Actions
- Review recent deployments to auth-service
- Increase database connection pool limits
- Add alerts for early auth latency spikes
