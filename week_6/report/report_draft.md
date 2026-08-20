# HW06 – API Testing Report

## 1. Cover Page and Student Information

- **Student ID:** 22127345
- **Assignment:** HW06 – API Testing
- **SUT:** EShop
- **Selected test tool:** Postman + Newman (provisional; default assignment tool)
- **Backend base URL:** `http://localhost:3000`
- **Backend status:** Started from `../eshop-SUT/backend/server.js`; verified on 20/08/2026.

## 2. Executive Summary

API 1 (`POST /api/login`) is complete through the **audit and extend** stages. The 40 AI-generated cases were human-reviewed and labeled (**37 VALID / 0 INVALID / 3 INCOMPLETE**); the three incomplete cases were corrected, and **6 student-authored cases (SLOGIN-001–006)** were added with an explanation of why the AI missed each. The audit (grounded by live requests against the running backend) also surfaced 7 candidate implementation bugs (lockout counting/timing, plaintext-password disclosure, account enumeration via lockout, and error-handling crashes), which will be confirmed and filed during the execution phase.

## 3. System Under Test and API Specification

The System Under Test is the EShop Vietnamese e-commerce demo application. The API specification is stored in `../eshop-SUT/api_specification.md`. The backend is implemented with Node.js, Express, and SQLite and listens at `http://localhost:3000`.

Initial connectivity evidence collected during setup:

- `GET /api/products` returned the seeded product list.
- `POST /api/login` with the seeded admin account returned a JWT and an admin user object.
- The `X-Student-Id: 22127345` header was included in the login verification request; the required pre-request-script console screenshot will be captured during the Postman execution phase.

## 4. Group API-Selection / Duplication Check

- **Student:** 22127345
- **Provisional three-API selection:** login, checkout, and admin order-status update.
- **Duplication check:** Pending confirmation from group members. This must be confirmed before test-case generation; no final claim of uniqueness is made yet.
- **Required evidence:** written confirmation or an equivalent group-selection record will be attached here.

## 5. Selected APIs

### 5.1 API 1 — Pool A

- **Feature:** FR-02 — Login and account lockout
- **Endpoint:** `POST /api/login`
- **Request body:** `{ "email": "...", "password": "..." }`
- **Expected success:** HTTP 200 with JWT token and user information.
- **Relevant negative/security scope:** invalid credentials, repeated failures and lockout, password handling, injection payloads, response disclosure, and token/schema validation.

### 5.2 API 2 — Pool B

- **Feature:** FR-08 — Checkout
- **Endpoint:** `POST /api/checkout`
- **Authentication:** JWT Bearer token required.
- **Request body in specification:** `{ "total_amount": 200000, "shipping_address": "..." }`
- **Expected behavior:** backend recalculates the order total from the cart, does not trust client-supplied `total_amount`, creates the order, and clears the cart after success.
- **Relevant negative/security scope:** unauthenticated access, tampered total, empty cart, invalid address, cart ownership/IDOR, and response-schema validation.

### 5.3 API 3 — Pool C

- **Feature:** FR-18 — Admin order management / order state transition
- **Endpoint:** `PUT /api/admin/orders/:id/status`
- **Authentication:** JWT Bearer token for an admin account.
- **Request body:** `{ "status": "confirmed" }`; allowed states are `pending`, `confirmed`, `shipping`, `delivered`, and `canceled`.
- **Expected behavior:** only valid transitions are accepted; terminal states cannot transition; users cannot perform admin operations; valid updates return the documented success response.
- **Relevant negative/security scope:** missing/invalid token, user-to-admin escalation, IDOR, invalid transitions, terminal-state transitions, malformed IDs/statuses, and response-schema validation.

## 6. Test Design and Coverage Strategy

The API 1 design applies equivalence partitioning, boundary value analysis, decision tables, state-transition testing, security/error guessing, and response-schema validation. The detailed strategy, conditions, and traceability artifacts are stored in [`artifacts/api1_login_test_strategy.md`](../artifacts/api1_login_test_strategy.md), [`artifacts/api1_login_test_conditions.md`](../artifacts/api1_login_test_conditions.md), and [`artifacts/api1_login_traceability.csv`](../artifacts/api1_login_traceability.csv).

### 6.1 Domain Partitions

The test design partitions known versus unknown emails, correct versus incorrect passwords, missing/null/empty/whitespace values, malformed and overlong emails, hostile payloads, and malformed protocol bodies. Boundary cases include the first, second, and third failed-login attempts and the lockout period.

### 6.2 State Transitions

The planned state model is `UNLOCKED → FAILED(1) → FAILED(2) → LOCKED → UNLOCKED after expiry`, with a successful login resetting the failure state. Stateful cases use an isolated account or a database reseed.

### 6.3 Security Requirements SEC-01–SEC-07

API 1 covers injection and hostile input resistance, account-enumeration resistance, brute-force lockout, JWT integrity, unexpected-field role escalation, sensitive response disclosure, and mandatory Student-ID header evidence. Exact SEC-01–SEC-07 wording will be reconciled against the course specification during human audit.

### 6.4 Response Schema Validation

The planned assertions verify HTTP status, required JSON keys and types, JWT syntax and identity claims, absence of a token on failure, and absence of plaintext passwords, reset tokens, lock metadata, or other unnecessary secrets.

## 7. API 1 Full Pipeline

### 7.1 Specification and Scope

API 1 is `POST /api/login` for FR-02. It accepts `email` and `password`, returns a JWT on success, rejects invalid credentials, and applies an account lockout after at least three consecutive failures. The request must include `X-Student-Id: 22127345`.

See [`artifacts/api1_login_test_strategy.md`](../artifacts/api1_login_test_strategy.md) and [`artifacts/api1_login_test_conditions.md`](../artifacts/api1_login_test_conditions.md).

### 7.2 AI Generation Process

The AI was instructed to derive test conditions before cases and to use the API specification plus the local implementation as test basis. It was instructed to cover every request parameter, FR-02 lockout transitions, security examples, schema validation, robustness, and the HW06 Student-ID requirement. The generated output is recorded in [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv).

### 7.3 AI-Generated Test Cases (Target: at least 35)

**Generated count: 40.** Cases span functional, negative, security, robustness, state-transition, schema, and traceability checks. After the human audit below, every row has been labeled `VALID` / `INVALID` / `INCOMPLETE` with reasoning recorded in the `HumanReview` column of [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv).

### 7.4 Human Audit: VALID / INVALID / INCOMPLETE

Every AI-generated case was reviewed against the SUT spec (`eshop-sut/api_specification.md` and `eshop-sut/README.md`, which defines the exact lockout rule and SEC-01–SEC-07) and the local implementation. The backend was started and key behaviors were verified directly (curl) to ground the audit. **Result: 37 VALID / 0 INVALID / 3 INCOMPLETE.**

- **VALID (37).** Cases whose expected results correctly match the specification. This includes the lockout cases: per the README the counter must increment by exactly **1** and lock after **3** consecutive failures for **30 s**, so LOGIN-025/026/027 encode the correct spec oracle even though the implementation deviates (see bugs below).
- **INVALID (0).** No AI case contradicted the specification outright; the AI's core oracles were sound.
- **INCOMPLETE (3) — corrected:**
  - **LOGIN-015** — `TestData` (“email longer than normal email limit”) and oracle were undefined (the spec sets no email length limit). Corrected to a concrete 300-character email with an explicit `no 500 / no stack trace / no token` oracle.
  - **LOGIN-029** — the “does not reveal unnecessary details” oracle was too vague and did not assert enumeration resistance. Corrected to require the locked-account response to be indistinguishable from an unknown-account response (generic 401), with no attempt/lock metadata or existence hint.
  - **LOGIN-034** — the oracle did not assert “no 500 / no stack trace”. Corrected to require a controlled 4xx. The verified behavior is a **500 TypeError with a full stack trace** for a `text/plain` body (genuine bug).

The audit also confirmed several genuine implementation bugs that the (correct) spec-based cases will detect at execution:

| # | Bug (verified) | Detected by |
|---|---|---|
| B1 | Failed-attempt counter increments by **2** instead of 1 (0 → 2 → 4) | LOGIN-025/026 |
| B2 | Account locks after **2** failures instead of 3 | LOGIN-026/027 |
| B3 | Lock duration is **180 s** instead of the required **30 s** | LOGIN-027 |
| B4 | Login response returns the **plaintext password** and lock metadata (`reset_token`, `login_attempts`, `locked_until`) — violates SEC-01/SEC-07 | LOGIN-039, SLOGIN-003 |
| B5 | Locked-account response (403 + “Tài khoản đã bị khóa”) is distinguishable from an unknown-account response (401) — **account-enumeration** weakness | SLOGIN-004, LOGIN-029 |
| B6 | `text/plain` content-type body causes a **500 crash** with a stack trace | LOGIN-034 |
| B7 | Malformed / wrong-shape JSON returns an **HTML error page leaking absolute file paths** | LOGIN-035, SLOGIN-006 |

These will be confirmed and filed as GitHub Issues during the execution phase.

### 7.5 Student-Added Test Cases (At least 5)

6 original student-authored cases (SLOGIN-001–006) were added — see [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv). Each targets a gap the AI missed, with the reason it was missed:

| ID | Focus | Why the AI missed it |
|---|---|---|
| SLOGIN-001 | Successful login **after lock expiry** (LOCKED → UNLOCKED by time) | The AI's state-transition graph stopped at “locked”; it never modelled the time-based expiry → UNLOCKED edge. |
| SLOGIN-002 | **Register → login** integration (FR-01 → FR-02) with a freshly created account | The AI generated cases per endpoint in isolation and assumed a pre-seeded “known user”; it never chained the primary registration→login happy path. |
| SLOGIN-003 | Hard schema assertion that `password` / `reset_token` / `login_attempts` / `locked_until` are **absent** from the response | AI's LOGIN-039 phrased disclosure generically and never pinned exact forbidden field names, so the plaintext password leak slipped through. |
| SLOGIN-004 | **Differential** check: locked-account vs unknown-account responses must be indistinguishable (enumeration resistance) | The AI tested “no enumeration” one path at a time (unknown email only) and never compared locked vs unknown responses. |
| SLOGIN-005 | Full unsupported-method set (GET/PUT/PATCH/DELETE) on a POST-only route | The AI only enumerated a single method (GET, LOGIN-037). |
| SLOGIN-006 | Non-object JSON bodies (array / number / string) handled safely | The AI tested malformed JSON and empty object but not well-formed JSON of the wrong shape. |

**Why each was missed (categories):** SLOGIN-001 and SLOGIN-002 are **API/model limitations** (state-graph and cross-endpoint reasoning the AI did not perform); SLOGIN-004, SLOGIN-005 and SLOGIN-006 are **prompt quality** issues (the AI covered only the obvious single-path variants); SLOGIN-003 is a **model limitation** (the AI trusted the documented `{token, user}` shape without auditing the real row payload).

### 7.6 Execution Results

### 7.7 Bugs Found and Links

## 8. API 2 Full Pipeline

### 8.1 Specification and Scope

### 8.2 AI Generation Process

### 8.3 AI-Generated Test Cases (Target: at least 35)

### 8.4 Human Audit: VALID / INVALID / INCOMPLETE

### 8.5 Student-Added Test Cases (At least 5)

### 8.6 Execution Results

### 8.7 Bugs Found and Links

## 9. API 3 Full Pipeline

### 9.1 Specification and Scope

### 9.2 AI Generation Process

### 9.3 AI-Generated Test Cases (Target: at least 35)

### 9.4 Human Audit: VALID / INVALID / INCOMPLETE

### 9.5 Student-Added Test Cases (At least 5)

### 9.6 Execution Results

### 9.7 Bugs Found and Links

## 10. Postman / Karate / RestAssured Features Used

## 11. Bug Summary

## 12. CI/CD Integration

### 12.1 Pipeline Configuration

### 12.2 All-Passing Sample Run

### 12.3 Intentionally Failing Sample Run

### 12.4 Screenshots and Links

## 13. AI-Driven API Test Generator

### 13.1 Design Overview

### 13.2 Self-Drawn Architecture Diagram

### 13.3 Pseudocode

### 13.4 Demonstration Video (Optional)

## 14. Test Summary

## 15. Limitations and Lessons Learned

## 16. References

## Appendix A — AI Prompt Log

## Appendix B — AI Audit Report

## Appendix C — AI Critique
