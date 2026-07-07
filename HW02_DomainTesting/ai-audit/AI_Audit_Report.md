# AI Audit Report

I use AI tools for the following tasks.

This AI Audit Report documents the user prompts provided during the session (setup and Features A–D) and the assistant's responses and actions. Each entry records: tool name (assistant), date, the user's prompt (excerpt or verbatim where noted), and the assistant output (verbatim or concise summary). Entries are grouped by phase/feature and by step (Extract / EP classes / TCs / BVA / Execute / Bugs / Gap).

Report date: 2026-07-07 (session)

----------
PHASE 0 — Persona & Ground Rules (AGENTS.md)
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompt (verbatim excerpt):
"You are a senior QA engineer with 20+ years of black-box functional testing experience...\nNon-negotiable rules for this whole assignment: 1. ORACLE = ONLY sut/README.md (the SRS) and sut/api_specification.md... 4. DUAL-CHANNEL VERIFICATION — every test case that has a UI path must be verified through BOTH the frontend UI AND the equivalent backend API call via curl..."
Assistant output (summary):
- Created `HW02_DomainTesting/AGENTS.md` with the ground rules and the five self-named risks.

----------
PHASE 0.5 — Environment Setup
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompt (verbatim excerpt):
"Create this folder structure in the workspace (empty files where noted): HW02_DomainTesting/... evidence/screenshot_inventory.md ... Show me the final tree before we continue."
Assistant output (summary):
- Verified and used the provided oracles (`README.md`, `api_specification.md`); updated evidence inventory later after screenshots were provided by the user.

----------
FEATURE A — FR-01: Account Registration (A1–A8)
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompt (excerpt):
"Extract every testable input and output for FR-01 – Account Registration. ... Stop for my review." Plus instructions for EP classes, Domain TCs, BVA, execution, bug reporting, gap analysis.
Assistant output (summary):
- FR-01 tasks are queued in the todo list; not yet executed in this session. Awaiting explicit user confirmation to proceed with FR-01 design/execution.

----------
FEATURE B — FR-08: Checkout (B1–B8)
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompt (excerpt):
"Extract every testable input and output for FR-08 – Checkout... Stop for review." (plus EP/BVA/Execute/Bug/Gaps instructions)
Assistant output (summary):
- FR-08 tasks entered in todo list; not yet executed in this session.

----------
FEATURE C — FR-19: User Management (Admin) (C1–C8)
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompts (selected verbatim/excerpts):
- C1: "Extract every testable input and output for FR-19 – User Management (Admin)..."
- C2: "Equivalence classes for FR-19: Caller role: admin token (valid) / non-admin user token (invalid) / no token (invalid) ..."
- C3–C6: design TCs, BVA, create Screenshot Plan, execute dual-channel verification. The user provided three screenshots and asked the assistant to begin black-box testing without reading source code.

Assistant outputs and actions (detailed summary):
- Read the oracles `README.md` and `api_specification.md` to define expected behavior.
- Ran black-box API tests (curl and Python urllib) from the workspace and recorded results, including:
	- `curl -I http://localhost:3000/api/admin/users` -> 401 Unauthorized without auth.
	- Attempts to `POST /api/login` using documented admin credentials returned 401.
	- Registered a disposable non-admin and observed login response includes `password` field in returned JSON.
	- With the non-admin token, `GET /api/admin/users` returned 200 OK (authorization bypass).
	- With non-admin token, `DELETE /api/admin/users/999999` returned 200 {"message":"User deleted"} (authorization bypass).
	- `POST /api/forgot-password` for `admin@eshop.com` returned 404 {"error":"User not found"}.

Files created/updated reflecting results:
- `HW02_DomainTesting/evidence/screenshot_inventory.md` — added S-001..S-003.
- `HW02_DomainTesting/reports/FR-19_UserManagement/domain_testing.md` — added domain test table and execution notes.
- `HW02_DomainTesting/reports/FR-19_UserManagement/boundary_value_analysis.md` — added BVA cases and observed failure.
- `HW02_DomainTesting/bug-reports/bug_report.md` — added BUG-001 and BUG-002.

Observations / Next actions recorded:
- Non-admin authorization bypass and return of plaintext password in login response are critical bugs; admin-token checks remain pending because the documented admin login failed.

----------
FEATURE D — FR-20: Mobile Profile Management (D1–D8)
----------
Tool: GitHub Copilot (assistant)
Date: 2026-07-07
User prompt (excerpt):
"Extract every testable input and output for FR-20 (Mobile) – Profile Management... Note explicitly: 'role' is NOT a documented field in the PUT body — that's exactly why it's a good tamper-test target..."
Assistant output (summary):
- FR-20 tasks queued; hybrid execution guidance provided. No FR-20 reports yet.

----------
Execution & Tool Usage Summary
----------
Representative commands executed during session:
- curl and Python calls to test auth and admin endpoints; results summarized earlier in this report.

Files created/modified in this session:
- `HW02_DomainTesting/AGENTS.md`
- `HW02_DomainTesting/evidence/screenshot_inventory.md` (S-001..S-003)
- `HW02_DomainTesting/reports/FR-19_UserManagement/domain_testing.md`
- `HW02_DomainTesting/reports/FR-19_UserManagement/boundary_value_analysis.md`
- `HW02_DomainTesting/bug-reports/bug_report.md`

----------
Open items & suggested next steps
----------
- Obtain or recover a working admin bearer token to complete admin-channel checks (self-delete, admin-only list enforcement). Options: attempt allowed API recovery flows or ask user to provide token.
- Proceed with FR-01 and FR-08 EP/BVA/TC creation and execution when user directs.
- The assistant can prepare GitHub issue drafts for BUG-001/BUG-002 and file them with the user's authorization.

Appendix — method and provenance

- All test design used only `README.md` and `api_specification.md` as the oracle. Black-box HTTP calls were used for execution; source code was not read for design.

If you want the audit expanded with full verbatim prompts and raw logs appended, say "Append verbatim logs"; to proceed to FR-01, say "Proceed FR-01".

End of AI Audit Report
