# API 1 Test Strategy — Login and Account Lockout

## 1. Scope and test basis

- **Requirement:** FR-02 — Login and account lockout.
- **Endpoint:** `POST /api/login`.
- **Base URL:** `http://localhost:3000`.
- **Request:** JSON object containing `email` and `password`.
- **Success oracle:** HTTP 200; response contains a JWT `token`, a success message, and user information.
- **Invalid-credential oracle:** HTTP 401 with a generic error message.
- **Lockout oracle:** after at least three consecutive failed attempts, subsequent login is rejected with HTTP 403 for the specified 30-second demo lock period and without revealing the detailed cause.
- **Required header:** `X-Student-Id: 22127345` on every request.
- **Out of scope:** registration, forgot-password, reset-password, authenticated resource authorization, UI validation, and actual email delivery.

## 2. Objectives and quality risks

| Risk | Impact | Likelihood | Priority | Mitigation / coverage |
|---|---|---:|---:|---|
| Valid users cannot log in | High | Medium | P0 | LOGIN-001/002, smoke execution |
| Failed attempts are counted incorrectly | High | High | P0 | LOGIN-025/026/027 and DB observation |
| Lockout duration or transition is wrong | High | High | P0 | LOGIN-027/028/029 |
| Password or sensitive user data is disclosed | High | Medium | P0 | LOGIN-039 and response-schema assertions |
| SQL injection or script payload changes behavior | High | Medium | P0 | LOGIN-016/017/022/023 |
| Input partitions cause server errors | Medium | Medium | P1 | LOGIN-006–015, 018–024, 034–036 |
| JWT is absent or malformed | High | Medium | P0 | LOGIN-031/032 and token decode/schema checks |
| Required student-identification evidence is missing | High | Medium | P0 | LOGIN-040 and Postman console screenshot |

## 3. ISTQB test-design techniques

| Technique | Application to API 1 |
|---|---|
| Equivalence Partitioning | Valid/invalid email, known/unknown account, correct/incorrect password, valid/invalid JSON and content type. |
| Boundary Value Analysis | Empty values, one-character values, minimum password length from the requirement, maximum/overlong inputs, and lock-at-third-failure boundary. |
| Decision Table Testing | Known account × correct/incorrect password × locked/unlocked state. |
| State Transition Testing | Unlocked → failed-attempt state → locked → unlocked after expiry; successful login resets failure state. |
| Experience-based / error guessing | SQL injection, XSS, Unicode, whitespace, duplicate requests, extra fields, malformed JSON, and secret disclosure. |
| Specification-based schema testing | Verify status, required keys, value types, JWT shape, and absence of forbidden sensitive fields. |

## 4. Test levels and types

- **Integration/system API testing:** primary level; exercises Express route, SQLite user state, and JWT creation together.
- **Functional:** successful login, invalid login, lockout, reset behavior, and error handling.
- **Security:** injection, script payloads, information disclosure, token integrity, brute-force/lockout behavior, and header traceability.
- **Reliability/robustness:** malformed, missing, null, empty, Unicode, and oversized inputs.
- **Performance smoke:** repeated normal login and lockout responses should complete within the agreed local threshold; record actual timing during execution.
- **Change-related:** rerun P0 smoke cases after any backend or seed-data change.

## 5. ISO/IEC 25010 focus

| Characteristic | Priority | Assessment |
|---|---|---|
| Functional suitability | Critical | Correct authentication and lockout rules. |
| Security | Critical | Confidentiality, authentication, brute-force resistance, injection resistance, and least disclosure. |
| Reliability | High | Deterministic state transitions and recovery after lock expiry. |
| Performance efficiency | Medium | Response time for normal and repeated attempts. |
| Compatibility | Medium | JSON/HTTP behavior and Postman/Newman interoperability. |
| Maintainability | Medium | Clear collection variables, reusable pre-request script, and traceable IDs. |
| Usability | Low for backend; medium for error messages | Generic, actionable error without account enumeration. |
| Portability | Low | Verify behavior against the documented local deployment. |

## 6. Environment and data strategy

- Node.js backend from `../eshop-SUT/backend`, SQLite seed database, and `http://localhost:3000`.
- Postman collection and environment variables: `baseUrl`, `studentId`, `testUserEmail`, `testUserPassword`, `adminEmail`, `adminPassword`.
- Credentials must be stored as local/CI variables and not committed in plaintext.
- Use a dedicated test account for lockout cases; restore or reseed the database between stateful cases.
- Capture request/response, response time, Postman console output, and Newman HTML output.

## 7. Entry and exit criteria

### Entry criteria

- Backend is running and reachable.
- API specification and selected API are confirmed.
- Group duplication check is complete.
- Test accounts and database-reset procedure are available.
- Postman collection includes the Student-ID pre-request script.

### Exit criteria

- At least 35 generated cases exist; this design contains 40.
- Every case has a requirement, technique, priority, precondition, steps, and observable oracle.
- Every AI case is human-labeled VALID / INVALID / INCOMPLETE and corrected where necessary.
- At least five student-authored cases are added separately.
- All P0 cases execute, results are recorded, and genuine defects are reported with evidence.

## 8. Implementation breakdown and estimates

| Task | Estimate | Dependency | Status |
|---|---:|---|---|
| Confirm API uniqueness and test data | 0.5 h | Group response | Pending |
| Review specification and implementation | 0.5 h | Backend available | Complete |
| Define partitions, decision table, and transitions | 1 h | Specification review | Complete |
| Generate and format 40 cases | 1 h | Design complete | Complete |
| Human audit and correction | 2 h | Generated cases | Pending |
| Add ≥5 original cases | 0.5 h | Human audit | Pending |
| Postman implementation and execution | 2 h | Test data and audit | Pending |
| Defect triage and evidence | 1 h | Execution | Pending |

