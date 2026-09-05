# API Gateway Troubleshooting Runbook

## Incident: HTTP 502 Bad Gateway (Upstream Timeout)
- **Root Cause:** The backend microservice (e.g., core-banking) took longer than 5000ms to respond or dropped the TCP handshake.
- **Remediation Steps:**
  1. Inspect network connectivity between the WSO2 API Gateway and upstream endpoints.
  2. Increase gateway endpoint timeout policy from 5s to 10s if backend batch workloads are active.
  3. Check backend CPU/Memory saturation.

## Incident: HTTP 429 Too Many Requests (Rate Limiting)
- **Root Cause:** A specific client exceeded their subscription tier quota or burst throttling limit.
- **Remediation Steps:**
  1. Identify the client ID/Application key from gateway analytics.
  2. If legitimate traffic spike, temporarily scale the tier policy on WSO2 API Manager admin portal.
  3. Advise client to implement exponential backoff retry.

## Incident: HTTP 401 Unauthorized (JWT Expired)
- **Root Cause:** Bearer token validity duration elapsed or OAuth token signing certificate rotated.
- **Remediation Steps:**
  1. Verify token issuer URL and key ID against Identity Server.
  2. Request client to refresh OAuth token via the token endpoint.