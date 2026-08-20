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
