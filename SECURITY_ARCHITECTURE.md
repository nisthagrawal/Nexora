# Security and trust architecture

Nexora is decision support for authorised border officers. It must not become a public identity-scoring service or an automated refusal system.

## Trust boundaries

```text
Officer device → API gateway → screening orchestrator → model services
                       │                 │                   │
                  OIDC + MFA         signed evidence      private network
                       │                 │
                  policy engine ← immutable audit hash → databases / watchlists
```

- **Authentication:** OIDC federation with MFA; short-lived access tokens; device and user identity recorded in each case.
- **Authorisation:** RBAC/ABAC: only a screened officer may open a case, only a supervisor may override it, and only audited service identities may query a watchlist.
- **Privacy:** encrypt images and PII in transit and at rest; keep keys in KMS/HSM; minimise retention; never store a biometric template or raw document on a public ledger.
- **Audit chain:** hash a canonical, redacted evidence record together with the preceding record hash. A permissioned ledger may anchor periodic hashes, but it is not a substitute for access control or a database. Corrections append an event; they never overwrite history.
- **Databases:** document/wanted/visa checks are server-side, jurisdiction-specific adapters. Cache only approved minimal responses with TTL. A demo must never claim access to government databases.

## Threat controls

| Threat | Control |
|---|---|
| altered scan / reprint | forensic model, MRZ and visual-field consistency, reviewer queue |
| replay/API abuse | nonce/idempotency key, rate limits, WAF, signed service requests |
| malicious file | MIME + magic-byte checks, size/pixel limits, malware sandbox, strip metadata |
| prompt/model input attack | isolated model services, strict schemas, no tool access from OCR text |
| model drift/unseen attack | versioned models, calibration, holdout monitoring, abstain/review policy |
| insider access | MFA, least privilege, field-level audit events, supervisor review |

## What the blockchain component is—and is not

It is a tamper-evident audit anchor for case/evidence hashes among authorised agencies. It does not validate a passport, train a model, store PII, or replace a secure relational case database.
