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
**Prompt**:
> I'm doing homework in week_6. Now after creating test cases, I need to verify VALID, INVALID and INCOMPLETE cases, and also add some test cases that AI missed as well as explanation. Now help me to do that according to the requirement, then update the checklist and modify prompt and audit logs to report that I've already corrected AI mistakes

**Artifact produced**: Updated `artifacts/api1_login_test_cases.csv` (all 40 rows labeled with reasoning, 3 INCOMPLETE cases corrected, 6 student cases SLOGIN-001–006 added), updated `artifacts/api1_login_traceability.csv`, `report/report_draft.md` (§7.3/7.4/7.5 + executive summary), `hw_requirements.md` checklist, and this prompt log.

**Human review / changes**: I verified each AI case against the SUT spec (`api_specification.md` + `README.md`, which defines the lockout rule and SEC-01–SEC-07) and the running backend via live requests. I corrected LOGIN-015 (undefined email-length test data), LOGIN-029 (vague no-enumeration oracle), and LOGIN-034 (weak no-500 oracle). I designed and added 6 cases (SLOGIN-001–006) the AI missed and documented why. The audit surfaced 7 candidate bugs (B1–B7: lockout counter +2, lock after 2 failures, 180s lock, plaintext-password disclosure, account enumeration via lockout, 500 crash on text/plain, HTML error-page file-path leak) to be confirmed and filed during the execution phase. I did not generate the execution evidence (Newman report / console screenshots), which remains manual.

---
