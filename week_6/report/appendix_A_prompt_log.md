# Appendix A — AI Prompt Log

Record every AI interaction used for HW06. Do not copy prompts from other students.

For each interaction, record:

- Date and time
- AI tool name
- Purpose / related API or artifact
- Exact prompt
- AI output or a link/path to the saved output
- Human review and changes made

| # | Date/time | AI tool | Purpose | Exact prompt | Output / artifact | Human review / changes |
|---|---|---|---|---|---|---|

## [16:06 20/08/2026] — Codex (GPT-5)
**Purpose**: HW06 setup and scope — record the student identity and local SUT base URL, identify suitable Pool A/B/C API selections, and update the report/checklist before test generation.
**Prompt**:
> studentID: 22127345
> 
> base url: you need to run backend in @../eshop-SUT 
> Help me to fill in the remaining parts

**Artifact produced**: Updated HW06 setup/scope in `report/report_draft.md` and progress items in `hw_requirements.md`; verified the local backend at `http://localhost:3000` with `GET /api/products` and an admin login request.

**Human review / changes**: The student must confirm the three provisional API selections with group members and replace the pending duplication-check item with real evidence. The Student-ID console screenshot and all execution evidence must be captured manually.

---

## [16:19 20/08/2026] — Codex (GPT-5)
**Purpose**: HW06 API 1 documentation, ISTQB test design, QA planning, and generation of at least 35 login test cases for Pool A / FR-02.
**Prompt**:
> Now help me to start with API 1. Apply $breakdown-test $qa-manual-istqb $qa-test-planner to complete the checklists related to documentation, design, and generate test cases for API 1

**Artifact produced**: API 1 login test strategy, test conditions, 40-case CSV test suite, traceability matrix, report documentation, and checklist updates.

**Human review / changes**: The cases are marked `AI-GENERATED / PENDING HUMAN AUDIT`. The student must review every case, assign VALID / INVALID / INCOMPLETE, correct cases, add at least five original cases, and confirm exact SEC-01–SEC-07 wording.

---

## [22:37 20/08/2026] — DeepSeek Harness (Claude Sonnet 4.6)
**Purpose**: HW06 API 1 (Pool A / FR-02) — human audit of the 40 AI-generated login test cases (label VALID / INVALID / INCOMPLETE, correct incomplete ones), and extension with student-authored cases the AI missed, plus checklist / prompt-log / audit-log updates. Serves HW06 requirement 2 (Audit) and 3 (Extend).
**Prompt**: A follow-up audit request to review and correct the AI-generated login cases; the exact wording is not reproduced here because this log records the correction work rather than the request.

**Corrections and additions I made (for the tutor):** I audited all 40 generated login cases against the SUT spec (`api_specification.md` + `README.md`, which fixes the lockout rule and SEC-01–SEC-07) and the running backend, and labeled them **37 VALID / 0 INVALID / 3 INCOMPLETE** with per-case reasoning. I corrected the three incomplete cases — LOGIN-015 (undefined email-length test data → concrete 300-char email), LOGIN-029 (vague no-enumeration oracle → require indistinguishability from an unknown-account response), and LOGIN-034 (weak oracle → require no 500 / no stack trace). I then added **6 student-authored cases the AI missed** (SLOGIN-001–006) and explained why the AI missed each: SLOGIN-001 lock-expiry recovery, SLOGIN-002 register→login integration, SLOGIN-003 hard response-secret-absence assertion, SLOGIN-004 locked-vs-unknown enumeration check, SLOGIN-005 full unsupported-method set, SLOGIN-006 non-object JSON bodies. The audit also surfaced 7 candidate bugs (B1–B7) that were later confirmed during execution.

---

## [00:35 21/08/2026] — Codex (GPT-5)
**Purpose**: Execute API 1 with Postman + Newman and produce the required execution evidence.
**Prompt**:
> OK so help me to execute the test cases using Postman + Newman

**Artifacts produced**: `artifacts/build_api1_postman_collection.mjs`, `artifacts/api1_login.postman_collection.json`, `artifacts/api1_newman_report.html`, and `artifacts/api1_newman_report.xml`.

**Execution result**: 48 requests, 162 assertions, 9 failed assertions across 6 requests. The collection pre-request script and Student-ID assertion ran on all 48 requests. Failures confirmed lockout behavior, unsafe `text/plain` handling, sensitive response disclosure, and lockout account enumeration. A manual Postman console screenshot and GitHub Issue screenshots remain outstanding.

---

## [05:40 21/08/2026] — Codex (GPT-5)
**Purpose**: Incorporate the student's Postman Runner screenshots and console/header evidence into the API 1 report and checklist.
**Prompt**:
> Chúng ta đã sử dụng test runner của postman để chạy nguyên collection. Minh chứng của việc chạy hết lên thì có 155 passed và 9 failed: [screenshots]. Giúp tôi fill vào report

**Artifact updated**: `report/report_draft.md`, `hw_requirements.md`, and `ai_compliance/audit_report.md`.

**Human evidence incorporated**: Postman Runner summary — 48 requests, 164 assertions, 155 passed, 9 failed, 0 errors; pre-request script, post-response assertions, console log, and request-header evidence showing `X-Student-Id: 22127345`. GitHub Issue screenshots remain pending.

---

## [current session 21/08/2026] — Codex (GPT-5)
**Purpose**: HW06 API 2 / Pool B design stage — complete the first six API 2 checklist actions for `POST /api/checkout`.
**Prompt**:
> $qa-test-planner $qa-manual-istqb $breakdown-test Design docs as suggested in API 2 - pool B in week_6/hw_requirements.md . Just do the first 6 actions

**Artifacts produced**: `artifacts/api2_checkout_test_strategy.md`, `artifacts/api2_checkout_test_conditions.md`, `artifacts/api2_checkout_test_cases.csv` (37 generated cases), `artifacts/api2_checkout_traceability.csv`, report §8.1–§8.3, and the first six API 2 checklist items.

**Human review / changes**: The six design requirements are now documented and traceable. The 37 cases remain `AI-GENERATED-PENDING-AUDIT`; VALID / INVALID / INCOMPLETE labeling, corrections, student extensions, execution, evidence, and GitHub bug filing are intentionally not marked complete.

---

## [23:15 21/08/2026] — Codex (GPT-5)
**Purpose**: Execute the audited API 2 checkout suite against the local SUT with Postman/Newman and produce execution evidence.

**Prompt**:
> tương tự giúp tôi execute test cases cho feature này

**Artifacts produced**: `artifacts/build_api2_postman_collection.mjs`, `artifacts/api2_checkout.postman_collection.json`, `artifacts/api2_newman_report.html`, and `artifacts/api2_newman_report.xml`.

**Execution result**: 48 requests (5 setup + 43 API cases), 121 assertions, 102 passed, 19 failed, 0 script errors. All 48 pre-request scripts logged and injected `X-Student-Id: 22127345`. Failures reproduced weak validation, client-total trust, lax Bearer scheme enforcement, empty-cart/duplicate checkout, `text/plain` 500/stack disclosure, numeric-field injection acceptance, and overlong-address acceptance. Manual Postman GUI screenshot and API 2 GitHub issue links remain pending.

### Prompt entry — API 2 Postman and GitHub evidence incorporated

**Date**: 2026-08-22
**Purpose**: Add the student's Postman Collection Runner result and API 2 GitHub Issue evidence to the report.

**Prompt**: “Màn hình kết quả chạy API 2 bằng postman … kết quả của các github issues … Giúp tôi dựa vào số thứ tự của issue tự construct luôn link tới github issue tương ứng và fill vào report.”

**Artifacts incorporated**: `artifacts/evidence/api2/01_postman_runner_api2.png`, `artifacts/evidence/api2/02_github_issues_api2.png`, and report §8.6–§8.7.

**Human evidence**: Postman Runner shows 121 tests, 102 passed, 19 failed, and 0 errors. The issue-list screenshot shows API 2 issues #70–#76. The report now links each issue using `https://github.com/pinkWar123/software-testing-group-06/issues/{number}`.

---

## [18:12 21/08/2026] — DeepSeek Harness (Claude Sonnet 4.6)
**Purpose**: HW06 API 2 (Pool B / FR-08) — human audit of the 37 AI-generated `POST /api/checkout` test cases (label VALID / INVALID / INCOMPLETE, correct incomplete ones) and extension with student-authored cases the AI missed. Serves HW06 requirements 2 (Audit) and 3 (Extend). The exact request wording is not logged here; this entry records the correction and extension work for the tutor.

**Corrections and additions I made (for the tutor):** I audited all 37 generated checkout cases against the spec (`api_specification.md` + `README.md`, which fixes FR-08 and SEC-01–SEC-07) and the checkout implementation, verifying key behaviors with live requests against the running backend. I labeled them **33 VALID / 0 INVALID / 4 INCOMPLETE** with per-case reasoning. I corrected the four incomplete cases — API2-005 (null total, vague oracle → forbid persisting a null total), API2-006 (string total, vague → forbid persisting a non-numeric total), API2-008 (zero total, vague → forbid a zero-priced persisted order), and API2-012 (wrong auth scheme → require that only `Bearer` is accepted). I then added **6 student-authored cases the AI missed** (SAPI2-001–006) and explained why the AI missed each: SAPI2-001 persisted total equals the cart line-item sum, SAPI2-002 double-submit idempotency, SAPI2-003 state read-back via `GET /api/orders/my-orders`, SAPI2-004 injection in the numeric `total_amount`, SAPI2-005 cross-user cart isolation, SAPI2-006 overlong-address length bound. The audit surfaced 6 candidate bugs (C1–C6: client total trusted, no input validation, cart not read/cleared + duplicates, Bearer scheme not enforced, 500 crash on `text/plain`, HTML error page leaking file paths) to be confirmed during execution.

---
