# API 3 Test Strategy — `PUT /api/admin/orders/:id/status`

## Basis and objective

- **Feature:** FR-18 Admin order management, constrained by FR-10 order state machine.
- **Endpoint:** `PUT http://localhost:3000/api/admin/orders/:id/status`.
- **Authentication:** `Authorization: Bearer <admin JWT>` and `X-Student-Id: 22127345`.
- **Request:** `{ "status": "confirmed" }`.
- **Allowed states:** `pending`, `confirmed`, `shipping`, `delivered`, `canceled`.
- **Success oracle:** HTTP 200 JSON `{ "message": "Order status updated" }` and the persisted order has the requested status.
- **Negative oracle:** controlled 4xx JSON response; no status mutation and no privilege or ownership bypass.

The test basis is `../eshop-SUT/api_specification.md`, the FR-10/FR-18 requirements in `../eshop-SUT/README.md`, and the local implementation in `../eshop-SUT/backend/server.js`. The implementation currently authenticates JWTs but does not visibly enforce `role = admin` in `authenticateToken`; this is recorded as a risk to verify, not as a completed defect.

## Scope

In scope: admin authentication and authorization, order-ID partitions, status partitions, valid and invalid transitions, terminal-state protection, ownership/IDOR, malformed JSON and content type, injection/error handling, response schema, persistence, and Student-ID header evidence.

Out of scope for this stage: human audit labels, corrections, student-added cases, execution, screenshots, and GitHub defect filing.

## ISTQB test design

| Technique | Application |
|---|---|
| Equivalence partitioning | Admin/user/invalid/missing JWT; existing/non-existing/malformed order IDs; allowed/unknown/null/empty/non-string statuses. |
| Boundary value analysis | IDs `0`, `1`, `-1`, very large integer, decimal, whitespace and maximum-length path values. |
| Decision table | Token validity × role × current order state × requested status determines 200, 401/403/404/400 and side effects. |
| State transition | `pending → confirmed → shipping → delivered`; `pending/confirmed → canceled`; `delivered` and `canceled` are terminal. |
| Experience-based/error guessing | IDOR, role escalation, SQL injection, prototype-like JSON keys, duplicate fields, malformed JSON, unsupported methods and wrong content type. |

## Risk and priority

| Risk | Impact | Priority | Mitigation/test focus |
|---|---|---|---|
| Non-admin JWT can update orders | Unauthorized operational and financial impact | Critical | API3-007–012, SAPI3-002 |
| Invalid transition accepted | Incorrect fulfillment/lifecycle state | Critical | API3-015–026 |
| ID/path injection or IDOR | Cross-order modification or data integrity loss | Critical | API3-004–006, API3-027–030 |
| Weak input/error handling | Crash, leakage, or inconsistent state | High | API3-031–036, SAPI3-004–005 |
| Response/persistence contract drift | Admin UI/client integration failure | High | API3-037–040, SAPI3-006 |

## Environment and data

- Node.js backend from `../eshop-SUT/backend/server.js`, SQLite seed database, base URL `http://localhost:3000`.
- Runtime-only variables: `baseUrl`, `studentId`, `adminToken`, `userToken`, `orderIdPending`, `orderIdConfirmed`, `orderIdShipping`, `orderIdDelivered`, and `orderIdCanceled`.
- Each stateful case uses an isolated order or restores the original status after verification. Do not commit credentials or tokens.
- Postman Collection Runner/Newman is the planned execution tool; collection-level pre-request logic will inject `X-Student-Id` and request assertions will validate status, JSON, persistence, and authorization.

## Entry and exit criteria for this design stage

**Entry:** API specification, state-machine rules, local implementation, and seeded order states are available.

**Exit:** The first six API 3 checklist items have traceable artifacts: specification, at least 35 generated cases, domain partitions, state model, security coverage, and response-schema oracle. Human audit and execution are intentionally not claimed complete.
