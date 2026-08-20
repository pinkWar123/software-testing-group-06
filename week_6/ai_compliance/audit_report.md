# AI Audit Report — HW06

## 1. AI Tools Used

- Codex (GPT-5): repository inspection, setup/scope drafting, checklist tracking, and audit-log drafting.

## 2. Interaction Log

For every AI interaction, include the tool name, date and time, exact prompt, and AI output.

- See **AI-02 Audit Entry 01** below and the corresponding entry in [`report/appendix_A_prompt_log.md`](../report/appendix_A_prompt_log.md).

## 3. Human Review and Corrections

Explain how each output was checked and identify corrections, omissions, invalid cases, and incomplete cases.

- The SUT path, API specification, backend URL, and endpoint details were checked against the local repository.
- The backend was started and its product-list and admin-login responses were checked.
- The API selections and group-duplication status remain subject to student confirmation.

## 4. AI-Assisted Artifacts and Traceability

List each artifact affected by AI and link it to the corresponding prompt-log entry and final file.

| Artifact | Prompt-log / audit reference | Final file |
|---|---|---|
| Setup and selected API scope | Prompt Log 01 / AI-02 Entry 01 | [`report/report_draft.md`](../report/report_draft.md) |
| Progress checklist | Prompt Log 01 / AI-02 Entry 01 | [`hw_requirements.md`](../hw_requirements.md) |

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
