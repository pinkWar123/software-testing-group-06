# Appendix A – AI Prompt Log

Record every real AI interaction used for this homework. Do not reconstruct or invent prompts after the fact. Add one entry immediately after each interaction and retain the original wording.

## Entry Template

### Prompt Entry [ID]

- **Date and time (Asia/Ho_Chi_Minh):**
- **AI tool and model:**
- **Purpose:**
- **Task/artefact affected:**
- **Prompt (verbatim):**
- **AI output or output reference:**
- **Human review and corrections:**
- **Final decision/use:**

---

## Entries

## [16:49 01/08/2026] — OpenAI Codex
**Purpose**: Task 1A – final compliance review of the shared GUI checklist
**Prompt**:
> Help me finalize task 1A

**Artifact produced**: Corrected the master checklist execution convention; completed verifiable reference citations; created the item-level human-review/AI-gap evidence template; identified historical prompt/provenance information that must not be fabricated.

---

## [22:57 03/08/2026] — OpenAI Codex
**Purpose**: Task 3 B1 – inspect the existing homework state and prepare supporting guidance for student-executed BrowserStack testing
**Prompt**:
> A previous agent produced the plan below to accomplish the user's task. Implement the plan in a fresh context. Treat the plan as the source of user intent, re-read files as needed, and carry the work through implementation and verification.
>
> # Task 3 B1 — AI-Assisted BrowserStack Execution
>
> ## Summary
>
> Complete only B1 `/dashboard` across five BrowserStack Live environments, then stop before committing so the student can review and partially stage the changes.
>
> The AI records must be truthful: they will state that AI researched BrowserStack, controlled or assisted the Live sessions, interpreted results, and drafted documentation. They cannot describe execution as research-only. The student will personally verify each live state and create the final screenshot with the identity overlay, satisfying the non-AI evidence boundary.
>
> ## B1 Execution
>
> 1. Pause for the student to create and verify a BrowserStack trial.
> 2. Launch five Live sessions:
>    - Windows 11 / Chrome / desktop
>    - Windows 11 / Edge / desktop
>    - Latest macOS / Firefox / desktop
>    - iPad / Safari / tablet
>    - Samsung Galaxy / Samsung Internet / phone
> 3. In every session:
>    - Student completes BrowserStack login and EMS SSO when prompted.
>    - AI opens `https://prod-dev.ems-fitus.cloud/dashboard`.
>    - Check page loading, carousel/cards, search, filters, navigation, readability, overflow, clipping, overlap, and responsive behavior.
>    - Record exact OS, browser version, device, resolution, Pass/Fail, and objective notes.
>    - Pause for the student to verify the live result, add `22127345-nhquan22@clc.fitus.edu.vn`, and capture the final screenshot.
>    - AI validates that the screenshot visibly contains the EMS page/URL, BrowserStack environment identity, device identity, and email overlay.
> 4. If Samsung Internet is unavailable, stop and request a coverage substitution rather than silently reducing the five-browser requirement.
> 5. Do not retain or stage automation code. Any temporary control helper stays ignored or under `/private/tmp`.
>
> BrowserStack Live provides interactive Windows, macOS, Android, and iOS coverage; its mobile environments are real devices. [BrowserStack Live](https://www.browserstack.com/docs/live/overview), [real-device confirmation](https://www.browserstack.com/support/faq/app-live/devices-and-operating-systems/do-you-provide-real-devices-for-interactive-app-testing)
>
> ## Evidence and Documentation
>
> After all five genuine B1 results exist:
>
> - Add five B1 rows to `compatibility_matrix.md`; mark B1 coverage complete while leaving B2/B4 unexecuted.
> - Store five final screenshots using `B1_E01_...` through `B1_E05_...`.
> - Draft report Sections 5.1–5.5 with the B1 strategy, matrix, counts, genuine defects, and screenshot index.
> - Follow the report skill: show the proposed report text and obtain approval before editing.
> - Reuse an existing finding ID when B1 reproduces an already logged defect; create a new finding only for genuinely distinct behavior.
> - Leave Google Form timestamps as `— (not submitted)` until the student actually submits them.
>
> ## AI Compliance Records
>
> - Add a prompt-log entry for the Task 3 planning request and another for the execution request, preserving each prompt verbatim.
> - Describe the purpose accurately as BrowserStack research, coverage planning, AI-assisted B1 Live execution, evidence validation, and report drafting.
> - Draft a standard five-section audit entry that distinguishes:
>   - AI actions: research, session control, compatibility analysis, matrix/report drafting.
>   - Student actions: account/SSO login, live-state verification, identity overlay, final screenshot capture, result approval.
> - Follow the audit skill: show the audit draft and obtain approval before appending it.
> - Mark the related Git commit as pending until the student creates the B1 commit.
>
> ## Validation and Stop Point
>
> Before stopping:
>
> - Confirm five B1 matrix rows and five valid screenshot paths.
> - Confirm five browser families, at least three OS families, and all three device classes.
> - Verify every screenshot manually with image inspection.
> - Run Markdown/path validation and `git diff --check`.
> - Show the exact changed-file list and a B1 Pass/Fail summary.
> - Do not run `git commit`.
>
> Because the worktree remains dirty, the student should use `git add -p` for the B1 report hunk and stage only the B1 compatibility screenshots, matrix changes, prompt-log entry, audit entry, and any genuine B1 finding changes. Existing `.gitignore`, Task 1 execution, and unrelated report changes remain unstaged.

**Artifact produced**: Repository and AI-compliance constraints were inspected, and BrowserStack Live was opened so the student could begin account setup. No compatibility test was executed or evaluated by AI, and no test result or screenshot was produced. The student corrected the proposed workflow before execution: the student will personally operate every Live session, inspect the EMS page, decide each result, add the identity overlay, and capture and verify every screenshot. Any later AI assistance is limited to organising authentic student-supplied results and drafting documentation for student review.

**Human review and correction**: The student rejected the prompt's proposed AI-assisted execution model and required student-only test execution. Therefore, the requested AI session control and AI evidence validation were not performed and must not be claimed in later documentation.

---
