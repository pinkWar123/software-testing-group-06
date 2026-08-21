# API 3 Test Conditions — Admin Order Status Update

## Domain partitions

| Parameter/condition | Valid partition | Invalid partitions | Boundaries / notes |
|---|---|---|---|
| JWT | Signed, unexpired admin token | Missing, empty, malformed, expired, forged, user token, wrong scheme | Authorization must require a valid admin identity. |
| `:id` path | Existing positive integer order ID | Missing, zero, negative, decimal, text, huge value, SQL-like payload, another user's order | Non-existing IDs must not mutate any record. |
| `status` | `pending`, `confirmed`, `shipping`, `delivered`, `canceled` when transition is allowed | Missing, null, empty, whitespace, unknown, case variant, number, array, object | Validate both value and transition from current state. |
| Current order state | `pending`, `confirmed`, `shipping`, `delivered`, `canceled` | Missing/corrupt database state | Delivered and canceled are terminal. |
| Header/body protocol | PUT + JSON + `X-Student-Id: 22127345` | Missing/wrong student ID, text/plain, malformed JSON, unsupported methods | Controlled 4xx; no stack trace or partial update. |

## State-transition conditions

1. `pending → confirmed` is accepted and persists `confirmed`.
2. `pending → canceled` is accepted and persists `canceled`.
3. `confirmed → shipping` is accepted and persists `shipping`.
4. `confirmed → canceled` is accepted and persists `canceled`.
5. `shipping → delivered` is accepted and persists `delivered`.
6. Any other transition from `pending`, `confirmed`, or `shipping` is rejected with no mutation.
7. `delivered → any state` and `canceled → any state` are rejected because both are final states.
8. Repeating the same request after a successful update must be rejected unless the state-machine explicitly treats it as idempotent; the oracle must be documented during audit.

## Security conditions SEC-01–SEC-07

| Requirement | API 3 condition/oracle |
|---|---|
| SEC-01 | The endpoint never accepts or returns passwords; response contains only the documented message. |
| SEC-02 | Missing, malformed, expired and forged JWTs are rejected before any order update. |
| SEC-03 | A valid JWT with `role=user` cannot perform the admin update; role must be checked, not merely token presence. |
| SEC-04 | Any user-controlled order/address data remains data; status update responses must not render HTML or execute payloads. |
| SEC-05 | SQL-like order IDs/statuses cannot alter the query or update an unintended order; database access must remain parameterized. |
| SEC-06 | Request fields such as `role: "admin"` cannot escalate the caller or alter authorization. |
| SEC-07 | The endpoint does not expose, create, or reuse OTP/reset secrets, tokens, or other unrelated credentials. |

## Schema and side-effect conditions

- Success must be JSON with exactly `message` as a string equal to `Order status updated`.
- Error responses must be JSON 4xx, contain a controlled `error` string, and not expose stack traces, absolute paths, SQL, credentials, or JWTs.
- A successful response must be followed by a read-back check proving that only the targeted order's `status` changed.
- A rejected request must leave the target order and all other orders unchanged.
