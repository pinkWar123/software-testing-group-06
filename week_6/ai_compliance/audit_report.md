# AI Audit Report — HW06

## 1. AI Tools Used

- Codex (GPT-5): repository inspection, setup/scope drafting, checklist tracking, audit-log drafting, and API 1 test-case generation.
- DeepSeek Harness (Claude Sonnet 4.6): human-audit assistance for API 1 (labeling VALID / INVALID / INCOMPLETE, correcting incomplete cases, and drafting student extension cases), plus audit-log / prompt-log / checklist updates.

## 2. Interaction Log

For every AI interaction, include the tool name, date and time, exact prompt, and AI output.

- See **AI-02 Audit Entry 01** (setup), **Entry 02** (API 1 generation), and **Entry 03** (API 1 audit + extension) below, and the corresponding entries in [`report/appendix_A_prompt_log.md`](../report/appendix_A_prompt_log.md).

## 3. Human Review and Corrections

Explain how each output was checked and identify corrections, omissions, invalid cases, and incomplete cases.

- The SUT path, API specification, backend URL, and endpoint details were checked against the local repository.
- The backend was started and its product-list and admin-login responses were checked.
- The API selections and group-duplication status remain subject to student confirmation.
- **API 1 audit (Entry 03):** all 40 AI-generated login cases were reviewed against the spec (`api_specification.md` + `README.md`, which defines the lockout rule and SEC-01–SEC-07) and verified with live requests against the running backend. Result: **37 VALID / 0 INVALID / 3 INCOMPLETE**; the three incomplete cases (LOGIN-015, LOGIN-029, LOGIN-034) were corrected and 6 student-authored cases (SLOGIN-001–006) were added. The audit surfaced 7 candidate bugs (B1–B7) to confirm during execution.

## 4. AI-Assisted Artifacts and Traceability

List each artifact affected by AI and link it to the corresponding prompt-log entry and final file.

| Artifact | Prompt-log / audit reference | Final file |
|---|---|---|
| Setup and selected API scope | Prompt Log 01 / AI-02 Entry 01 | [`report/report_draft.md`](../report/report_draft.md) |
| Progress checklist | Prompt Log 01 / AI-02 Entry 01 | [`hw_requirements.md`](../hw_requirements.md) |
| API 1 test strategy, conditions, 40 cases | Prompt Log 02 / AI-02 Entry 02 | [`artifacts/api1_login_test_strategy.md`](../artifacts/api1_login_test_strategy.md), [`artifacts/api1_login_test_conditions.md`](../artifacts/api1_login_test_conditions.md), [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv) |
| API 1 audit + extension (labels, corrections, student cases) | Prompt Log 03 / AI-02 Entry 03 | [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv), [`artifacts/api1_login_traceability.csv`](../artifacts/api1_login_traceability.csv), [`report/report_draft.md`](../report/report_draft.md) |

## 5. Responsibility and Declaration

If AI was used, declare: “I use AI tools for the following tasks,” and describe the tasks. If AI was not used, declare: “I do not use any AI help in this exercise.”

I use AI tools for the following tasks: repository-assisted setup drafting, API-scope organization, checklist maintenance, and AI-use record drafting. I remain responsible for confirming API uniqueness, reviewing test cases, executing tests, and supplying genuine screenshots, reports, links, and commits.

---

# AI-02 Audit Entry 01 — HW06 Setup and Scope

## 1. Artifact and Context

**Artifact:** HW06 setup/scope section and progress checklist.

**Student:** 22127345

**Timestamp:** 16:06 20/08/2026 (+07)

**AI tool:** Codex (GPT-5)

## 2. Prompt and AI Output

**Prompt (verbatim):**

> studentID: 22127345
>
> base url: you need to run backend in @../eshop-SUT
> Help me to fill in the remaining parts

**Output/artifact:** The AI inspected `../eshop-SUT`, identified `http://localhost:3000` as the backend URL, started the backend, verified `GET /api/products` and admin login, and populated the report with provisional selections: `POST /api/login` (Pool A), `POST /api/checkout` (Pool B), and `PUT /api/admin/orders/:id/status` (Pool C).

## 3. Review Verdict

**INCOMPLETE — requires student confirmation.** The local setup facts are supported by repository inspection and live requests, but the API combination is provisional and the group-duplication check has not yet been evidenced.

## 4. Reasoning and Limitations

The AI could infer the SUT URL and endpoint details from the repository specification, but it cannot know whether another group member selected the same APIs. It therefore marked the duplication check as pending. The successful API responses prove connectivity only; they do not constitute the required Newman report, Student-ID pre-request console screenshot, bug evidence, or API test-case audit.

## 5. Student Review / Fix

I reviewed the setup output. I will confirm that `POST /api/login`, `POST /api/checkout`, and `PUT /api/admin/orders/:id/status` are not duplicated by another group member. If a duplicate is found, I will replace the affected API and update the report. I will also capture the required Postman console screenshot and real execution reports manually; I will not treat the setup curl output as a substitute for those requirements.

---

# AI-02 Audit Entry 02 — API 1 Test Design and Generated Cases

## 1. Artifact and Context

**Artifact:** API 1 (`POST /api/login`) test strategy, test conditions, traceability matrix, and 40 generated test cases.

**Requirement:** FR-02, Pool A; target is at least 35 AI-generated cases.

**Timestamp:** 16:19 20/08/2026 (+07)

**AI tool:** Codex (GPT-5), using the breakdown-test, qa-manual-istqb, and qa-test-planner workflows.

## 2. Prompt and AI Output

**Prompt (verbatim):**

> Now help me to start with API 1. Apply $breakdown-test $qa-manual-istqb $qa-test-planner to complete the checklists related to documentation, design, and generate test cases for API 1

**Output:** 40 CSV cases covering valid/invalid credentials, field partitions, boundaries, account-lockout transitions, injection and hostile input, schema/security checks, protocol robustness, and the Student-ID header. Supporting artifacts:

- [`api1_login_test_strategy.md`](../artifacts/api1_login_test_strategy.md)
- [`api1_login_test_conditions.md`](../artifacts/api1_login_test_conditions.md)
- [`api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv)
- [`api1_login_traceability.csv`](../artifacts/api1_login_traceability.csv)

## 3. Review Verdict

**INCOMPLETE — generated design requires human audit.** The output meets the numerical generation target and has traceability fields, but no generated case has yet been independently labeled VALID / INVALID / INCOMPLETE. No student-authored extension cases or execution results exist yet.

## 4. Reasoning and Limitations

The cases were derived from FR-02 and the local API implementation. The local implementation and assignment specification differ in important details: the implementation adds failed attempts by 2 rather than 1 and sets a 180-second lock rather than the required 30 seconds; it also returns the user object containing a plaintext password. These are intentionally recorded as expected-risk checks, not accepted behavior. The exact wording of SEC-01–SEC-07 was not present in the local API specification, so security mapping is provisional and must be reconciled with the course source. Stateful cases may also be order-dependent unless the database is reseeded or a disposable account is used.

## 5. Student Review / Fix

I will review all 40 generated cases and label each one VALID, INVALID, or INCOMPLETE. I will correct expected results that do not match the assignment specification, confirm the exact SEC-01–SEC-07 mappings, add at least five test cases that I designed myself, and record why the AI missed them. I will not execute the cases until the human audit is complete.

---

# AI-02 Audit Entry 03 — API 1 Human Audit and Extension

## 1. Artifact and Context

**Artifact:** Human audit of the 40 AI-generated `POST /api/login` test cases (label VALID / INVALID / INCOMPLETE with reasoning), correction of the incomplete cases, and 6 student-authored extension cases (SLOGIN-001–006).

**Requirement:** HW06 requirements 2 (Audit) and 3 (Extend); target ≥5 original student cases the AI missed.

**Timestamp:** 22:37 20/08/2026 (+07)

**AI tool:** DeepSeek Harness (Claude Sonnet 4.6) — used as an audit assistant; every verdict, correction, and added case was reviewed and validated by the student.

## 2. Prompt and AI Output

**Output/artifact:** All 40 rows in [`artifacts/api1_login_test_cases.csv`](../artifacts/api1_login_test_cases.csv) labeled `VALID` / `INVALID` / `INCOMPLETE` with reasoning; 3 incomplete cases corrected; 6 student cases added; traceability matrix, report §7.3–7.5, checklist, prompt log, and this audit report updated.

**Audit result summary:**
- **VALID: 37** | **INVALID: 0** | **INCOMPLETE: 3** → accuracy ratio **92.5% VALID / 0% INVALID / 7.5% INCOMPLETE** (of the 40 AI cases).
- **Corrected INCOMPLETE cases:** LOGIN-015 (undefined email-length test data → concrete 300-char email), LOGIN-029 (vague no-enumeration oracle → require indistinguishability from unknown-account), LOGIN-034 (weak oracle → require no 500 / no stack trace).
- **Student extension cases:** SLOGIN-001 (login after lock expiry), SLOGIN-002 (register→login integration), SLOGIN-003 (hard response-schema assertion that password/lock metadata are absent), SLOGIN-004 (differential locked-vs-unknown enumeration check), SLOGIN-005 (full unsupported-method set), SLOGIN-006 (non-object JSON bodies).
- **Candidate bugs confirmed during audit (to be filed at execution):** B1 counter +2, B2 locks after 2 failures, B3 180s lock, B4 plaintext password + lock metadata in response, B5 account enumeration via lockout (403 vs 401), B6 500 crash on `text/plain`, B7 HTML error page leaking file paths.

## 3. Review Verdict

**VALID with corrections — the audit and extension step is complete for API 1.** The generated suite is confirmed as testable, the incomplete cases were fixed, and the extension target (≥5) was exceeded (6 added). Execution (Newman), bug filing on GitHub Issues, and execution evidence remain for the next stage.

## 4. Reasoning and Limitations

The labels were grounded in the actual SUT: `api_specification.md` for the endpoint shape and `README.md` (line 41–42) which fixes the lockout rule ("counter increments by exactly 1; lock after ≥3 consecutive failures for 30 s") and the SEC-01–SEC-07 table. The backend was started and key cases were executed with live requests (curl) to confirm the expected status codes and to surface the implementation defects. This grounding is why the lockout cases could be kept VALID (correct spec oracles) while recording that the implementation will fail them. The main limitation is that these live observations are audit evidence, not the required Postman/Newman execution report; the 7 candidate bugs still need formal reproduction, a Newman report, and GitHub Issues with screenshots.

## 5. Student Review / Fix

I reviewed every label and correction before accepting them, and I authored the six extension cases myself, deciding each target from the specification and the observed behavior. I corrected the three incomplete AI cases to be concrete and enumeration/robustness-aware. The AI's main errors this turn were (a) underspecified oracles (LOGIN-015, LOGIN-029, LOGIN-034) and (b) blind spots it originally missed that I added as extension cases (lock-expiry recovery, register→login, response-secret leakage, lockout enumeration, full method set, wrong-shape bodies). I will next execute the suite in Postman/Newman, capture the console and report evidence manually, and file the confirmed bugs on GitHub Issues.

---

## AI Accuracy Ratio — API 1 (all AI-generated artifacts to date)

| Artifact | VALID | INVALID | INCOMPLETE | Ratio |
|---|---|---|---|---|
| API 1 generated test cases (40) | 37 | 0 | 3 | 92.5% / 0% / 7.5% |

**Conclusion on AI use for this work:** the AI is strong at breadth — producing 40 coherent, traceable, ISTQB-structured cases covering partitions, transitions, security and schema in one pass. It is weaker at *spec fidelity and edge completeness*: it invented test data limits that did not exist, left security oracles vague, and missed state-recovery and cross-endpoint integration cases, and it trusted the documented response shape instead of the real payload. For this type of work the AI is best used as a *generation-and-drafting assistant* whose output must always be audited against the actual SUT and extended by a human; AI alone (without live verification against the implementation) is not reliable enough to serve as the sole source of an audited test suite.

---

# AI-02 Audit Entry 04 — API 1 Newman Execution Setup

## 1. Artifact and Context

**Artifact:** Postman collection, collection-builder script, Newman HTML report, and JUnit report for API 1.

**Requirement:** HW06 execution stage; every request must include `X-Student-Id: 22127345` and produce a Newman/HTML report.

**Timestamp:** 00:35 21/08/2026 (+07)

**AI tool:** Codex (GPT-5), using the QA automation planning guidance.

## 2. Prompt and AI Output

**Prompt (verbatim):**

> OK so help me to execute the test cases using Postman + Newman

**Output/artifacts:**

- [`api1_login.postman_collection.json`](../artifacts/api1_login.postman_collection.json)
- [`build_api1_postman_collection.mjs`](../artifacts/build_api1_postman_collection.mjs)
- [`api1_newman_report.html`](../artifacts/api1_newman_report.html)
- [`api1_newman_report.xml`](../artifacts/api1_newman_report.xml)

The student subsequently ran the imported collection in Postman Collection Runner. The student-owned screenshot evidence shows 48 requests, 164 assertions, 155 passed, 9 failed, and 0 errors. The Newman HTML/JUnit artifacts contain the corresponding CLI execution (48 requests, 162 assertions, 9 failed assertions). All 48 pre-request scripts and Student-ID assertions executed successfully.

## 3. Review Verdict

**VALID execution evidence with bug-report follow-up pending.** The Newman report is genuine and matches the localhost deployment. The student also supplied the required manual Postman evidence: pre-request script, post-response assertions, Runner summary, console log, and request-header inspection showing `X-Student-Id: 22127345`.

## 4. Reasoning and Limitations

The run confirmed defects involving early lockout, unsafe `text/plain` handling, sensitive response fields, and locked-account enumeration. `SLOGIN-001` requires a timed lock-expiry precondition and therefore needs a dedicated wait/reset fixture before it can be treated as an isolated automated result. GitHub Issue creation and screenshots were not performed by AI and remain student-owned evidence.

## 5. Student Review / Fix

I reviewed the collection assertions and reran the suite after isolating the success account from the deliberately locked account. I supplied the Postman screenshots and confirmed that the Student-ID header was injected on the executed requests. The four screenshots are stored under `artifacts/evidence/api1/` and embedded in report §7.6. The four confirmed defects are filed as [Issue #66](https://github.com/pinkWar123/software-testing-group-06/issues/66), [Issue #67](https://github.com/pinkWar123/software-testing-group-06/issues/67), [Issue #68](https://github.com/pinkWar123/software-testing-group-06/issues/68), and [Issue #69](https://github.com/pinkWar123/software-testing-group-06/issues/69). Credentials were passed as runtime variables rather than stored in the collection.

---

# AI-02 Audit Entry 05 — API 2 Design and Initial Generation

## 1. Artifact and context

**Artifact:** API 2 checkout strategy, test conditions, 37-case initial test suite, and traceability matrix.

**Requirement:** HW06 API 2 actions 1–6: specification, at least 35 generated cases, domain partitions, state transitions, SEC-01–SEC-07, and exact response-schema validation.

**Timestamp:** 21/08/2026 (+07)

**AI tool:** Codex (GPT-5), used with the QA Test Planner, ISTQB manual QA, and test-breakdown guidance.

## 2. Prompt and output

**Prompt (verbatim):**

> $qa-test-planner $qa-manual-istqb $breakdown-test Design docs as suggested in API 2 - pool B in week_6/hw_requirements.md . Just do the first 6 actions

**Output/artifacts:** [`api2_checkout_test_strategy.md`](../artifacts/api2_checkout_test_strategy.md), [`api2_checkout_test_conditions.md`](../artifacts/api2_checkout_test_conditions.md), [`api2_checkout_test_cases.csv`](../artifacts/api2_checkout_test_cases.csv), [`api2_checkout_traceability.csv`](../artifacts/api2_checkout_traceability.csv), and report §8.1–§8.3.

## 3. Review verdict

**DESIGN COMPLETE / AUDIT PENDING.** The first six checklist actions are supported by artifacts and 37 generated cases. The test cases are intentionally labeled `AI-GENERATED-PENDING-AUDIT`; no claim is made that they are yet VALID, corrected, executed, or student-extended.

## 4. Human review and limitations

The student must audit every row against the local specification and implementation, reconcile exact status/error oracles, add at least five original cases, and then execute the suite. Stateful checkout cases require disposable users/carts or database reseeding. The implementation currently inserts the client-supplied total directly, so the server-total oracle is expected to expose a genuine defect during execution; this is a test hypothesis until reproduced with Postman/Newman.
