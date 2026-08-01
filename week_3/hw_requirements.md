# HW03 Requirements Checklist and Work Plan

Source: `GUI_usability.md` (EMS edition). Duration: 10 hours. Deadline: Moodle submission link. This is a group assignment with one shared checklist and one individual scenario/report per member.

## 1. Setup, Scope, and Working Rules

- [ ] Confirm a group of 3–4 students and record members/responsibilities. **[Mandatory; no separate points]**
- [ ] Assign each member exactly one scenario (A, B, C, or D). **[Mandatory; no separate points]**
- [ ] Obey the no-duplication rule: no two members own both the same scenario and the same screen set; if a scenario is shared, select different screens. **[Mandatory; no separate points]**
- [ ] For the chosen scenario, list and justify at least 3 screens from the same function group. **[Required across Tasks 1B–3]**
- [ ] Use the same ≥3 selected screens for checklist execution, user testing, and compatibility testing. **[Required across Tasks 1B–3]**
- [ ] Create personal student/lecturer/guest accounts for user-side Scenarios B/D; do not share one group user account. **[Mandatory]**
- [ ] Confirm the admin account has the ADMIN role when using Scenarios A/C or the admin side of D. **[Mandatory]**
- [ ] Capture evidence during testing because ngrok-hosted EMS data may reset. **[Mandatory]**
- [ ] Document the entire working process in text-based form such as Markdown. **[Mandatory]**
- [ ] Review every AI-produced result and correct/refine it; do not submit raw AI output. **[Mandatory]**

## 2. Task 1A – Shared GUI Checklist (15 points, group)

- [ ] Produce one shared GUI checklist with **more than 40 items**. **[15 points, with the following Task 1A items]**
- [ ] Cover all four interface aspects: IA-01 General UI standards, IA-02 Forms, IA-03 Navigation, and IA-04 Feedback/state.
- [ ] Ground the checklist in Nielsen’s 10 heuristics, Norman’s 6 principles, Shneiderman’s 8 golden rules, per-widget course checklists, and other documented references.
- [ ] Use an AI tool to generate an initial checklist set.
- [ ] Critically review and revise the AI-generated set as a group.
- [ ] Add original human-reviewed checklist items.
- [ ] For every item added beyond the AI output, explain why AI missed it (for example: prompting limits, model limits, or EMS-specific behavior).
- [ ] Consider commonly missed coverage such as accessibility, RTL layout, dark mode, keyboard navigation, and EN/VI internationalisation.
- [ ] Submit the final shared checklist in Excel or Markdown.
- [ ] Submit a reference-sources list (books, articles, standards, and course slides).
- [ ] Submit the AI prompts used to generate and refine the shared checklist.
- [ ] Submit the group artefacts once per group and keep a copy in every member’s submission.

## 3. Task 1B – Per-Screen Checklist Execution (15 points, individual)

- [ ] Execute the complete shared checklist on each of the chosen ≥3 screens. **[15 points, with the following Task 1B items]**
- [ ] Mark every checklist item **Passed** or **Failed** for every screen.
- [ ] Include a Notes column.
- [ ] For every Failed result, state the failure reason in Notes.
- [ ] Attach real EMS screenshots for Failed items only.
- [ ] Report every discovered bug in the main report.
- [ ] For every bug include screen, reproduction steps, expected result, actual result, severity, and screenshot.
- [ ] Also send every bug through the Google Form required by §7.

## 4. Task 2 – Five-Participant User Test and Usability Report (25 points, individual)

### Phase 1 – Design and Prepare

- [ ] Write a realistic, goal-oriented task scenario spanning the selected ≥3 screens; specify the goal without step-by-step clicks. **[25 points, with all Task 2 items]**
- [ ] Define task success as completed/partial/failed.
- [ ] Measure time on task.
- [ ] Measure error/hesitation count.
- [ ] Select and administer either SUS or UEQ-S after the task.
- [ ] Prepare open-ended probes covering clarity, error recovery, speed, and trust.
- [ ] Recruit exactly 5 real participants matching the target-user profile.
- [ ] Recruit participants from outside this class.
- [ ] Keep verifiable contacts (Zalo/email/phone) and mask the middle four digits in submitted tables.
- [ ] Run one additional pilot participant before the five real sessions.
- [ ] Record what the pilot exposed and how the scenario/procedure was refined.

### Phase 2 – Run Five Sessions

- [ ] Tell each participant that the product—not the participant—is being tested.
- [ ] Ask each participant to think aloud.
- [ ] Observe neutrally without leading hints; intervene only if completely stuck.
- [ ] Obtain consent before recording screen/audio.
- [ ] Record the screen and audio where consent permits.
- [ ] Take structured notes on friction, errors, hesitations, and verbalised frustration.
- [ ] Collect the selected SUS/UEQ-S responses after every session.
- [ ] Ask the prepared probe questions after every session.

### Phase 3 – Analyse and Report

- [ ] Score SUS/UEQ-S for all five participants.
- [ ] Tabulate success rate, mean time, and errors.
- [ ] Group similar pain points.
- [ ] Separate isolated bugs from systemic design issues.
- [ ] Rank findings by severity from 0–4.
- [ ] Produce a Usability Report containing the task scenario.
- [ ] Include a masked five-participant table.
- [ ] Include the metrics table.
- [ ] Include ranked findings with one real screenshot for each finding.
- [ ] Include a prioritised list of concrete recommendations.
- [ ] Send genuine bugs/usability findings through the §7 Google Form and reconcile them with the aggregate log.

### Task 2 Integrity

- [ ] **⚠️ MUST NOT USE AI:** Do not generate, fabricate, or impersonate the five participants or their identities/contact details.
- [ ] **⚠️ MUST NOT USE AI:** Do not generate or fabricate consent, raw session observations, responses, scores, recordings, or metrics.
- [ ] Be prepared for the TA to call up to two participants; impersonation results in **0/25 for Task 2**.

## 5. Task 3 – Cross-Browser/Cross-Platform Testing (25 points, individual)

- [ ] Build a compatibility matrix for each selected screen. **[25 points, with all Task 3 items]**
- [ ] Cover 3 operating systems per screen (for example Windows, macOS, and Android/iOS).
- [ ] Cover 5 browsers per screen (for example Chrome, Firefox, Safari, Edge, and Opera/Samsung Internet).
- [ ] Cover 3 device classes per screen: desktop, tablet, and phone.
- [ ] The matrix may be a covering set rather than all 45 combinations, but every OS, browser, and device class must appear at least once **for each screen**.
- [ ] Clearly identify every tested cell and mark it Pass or Fail.
- [ ] Prefer a BrowserStack or LambdaTest trial; if unavailable, use another cloud service or real physical devices.
- [ ] Ensure every screenshot clearly shows browser, OS, device name, and the EMS URL.
- [ ] Capture a real screenshot for **every covered matrix cell**.
- [ ] Overlay the tester’s student-ID email in the form `MSSV@....edu.vn` on every cross-platform screenshot.
- [ ] For every rendering/layout Fail, attach the screenshot and a concise defect note (for example overflow, overlap, broken layout, unreadable text, or non-responsive control).
- [ ] **⚠️ MUST NOT USE AI:** Do not generate or fabricate cross-platform screenshots, tested states, identity labels, URLs, or browser/OS/device evidence.

## 6. Findings Submission and Aggregate Log (10 points, individual)

- [ ] Submit **every defect and usability improvement from Tasks 1–3** individually to the required Google Form. **[10 points, with all findings-channel items]**
- [ ] Use the requested student-ID email so each submission is attributable.
- [ ] Aggregate all submitted findings into one Bug & Usability Findings Log.
- [ ] Include at minimum: ID; Scenario/Screen; Type (Bug/Usability); Description; Steps/Heuristic; Severity; Suggested fix; Screenshot ref; Form-submission timestamp.
- [ ] Keep the aggregate log and Google Form submissions consistent; reconcile their counts.
- [ ] **⚠️ MUST NOT USE AI:** Do not fabricate a Google Form submission, timestamp, screenshot reference, or reported live-system result.

## 7. Agent Skills (10 points)

- [ ] Submit reusable Agent Skills for GUI-checklist execution, heuristic usability evaluation, and compatibility-matrix runs. **[10 points]**
- [ ] Submit demonstration video links (YouTube) showing end-to-end skill use on a complete screen or flow.

## 8. Mandatory AI Compliance

- [ ] Declare every AI tool used in the AI Audit Report.
- [ ] If no AI was used, include exactly: “I do not use any AI help in this exercise.”
- [ ] If AI was used, include: “I use AI tools for the following tasks,” followed by the tasks.
- [ ] For every AI interaction record tool, date/time, prompt, and AI output.
- [ ] Include the group-checklist prompts in the AI Audit Report/prompt log.
- [ ] Attach the AI Audit Report as a mandatory appendix.
- [ ] Write and attach a **200–300 word** AI Critique covering a real error/bias/omission, why AI missed it, and the collaboration principle learned.
- [ ] Demonstrate Bloom-AI G9.3 (Analyse) and G9.4 (Collaborate with AI for exploratory testing).

## 9. Anti-AI-Cheat and Academic Integrity

- [ ] **⚠️ MUST NOT USE AI:** Do not generate/fabricate per-screen checklist-execution evidence or actual EMS screen states.
- [ ] **⚠️ MUST NOT USE AI:** Do not generate/fabricate cross-platform captures or the required email/browser/OS/device/URL evidence.
- [ ] **⚠️ MUST NOT USE AI:** Do not generate/fabricate participants or raw user-test data.
- [ ] Do not copy another student’s individual work or prompts; copying, including prompts, gives both parties a grade of 0.
- [ ] Only the group’s shared checklist is expected to be identical across members; screen selection, execution, usability work, compatibility work, and findings must be individual.

## 10. Git History and Oral Defense

- [ ] Create a new Git commit for each testing step (for example checklist design, execution per screen, bug logging, heuristic evaluation, and each compatibility run).
- [ ] Export and submit the Git commit log as a text file.
- [ ] Be ready for possible selection among 30% of students for a 5–7 minute oral defense in the following week.

## 11. Final Files and Packaging

- [ ] Produce the main report in both Markdown and PDF, including scenario, ≥3 screens and rationale, per-screen execution, Usability Report, and compatibility report.
- [ ] Include user-testing scenario, five-person masked participant table, per-session notes, SUS/UEQ-S responses, metrics, and available recordings.
- [ ] Include the Bug & Usability Findings Log consistent with Google Form submissions.
- [ ] Include every required cross-platform screenshot with the student-email overlay.
- [ ] Include the AI Critique in Markdown and PDF.
- [ ] Include the AI Audit Report in Markdown and PDF.
- [ ] Include the Git commit log text file.
- [ ] Include Agent Skills and demo-video links.
- [ ] Create `README.md` with the rubric self-assessment table.
- [ ] In `README.md`, summarize: chosen scenario; screens; checklist items designed/executed/passed/failed; bug count; five participants; usability findings by severity; compatibility cells; demo videos.
- [ ] Include all other supporting material.
- [ ] Name the archive `<StudentID>_HW03_AI_GUIUsability_EMS_<SelfAssessedGrade>.zip`.
- [ ] Use a three-digit self-assessed grade from `000` to `100` (example: `25127001_HW03_AI_GUIUsability_EMS_090.zip`).
- [ ] Submit the group folder plus one report per member through Moodle.
- [ ] Submit before the Moodle deadline; late submission is not permitted.
- [ ] Verify every required document is present; a missing required document results in **0 points**.

## 12. Score Checklist

| Criterion | Points |
| --- | ---: |
| Task 1A – Shared checklist, references, and AI prompts | 15 |
| Task 1B – Per-screen execution and bug reports | 15 |
| Task 2 – Five-user test and Usability Report | 25 |
| Task 3 – Compatibility matrix | 25 |
| Google Form findings and aggregate log | 10 |
| Agent Skills and demonstrations | 10 |
| **Total** | **100** |

## 13. AI Assistance Boundaries

| What AI can help with | What must be performed and verified manually |
| --- | --- |
| Draft and refine the >40-item checklist, provided the group critically reviews it | Choose individual scenario/screens and coordinate no-duplication with the group |
| Suggest reference-based checklist categories and identify likely omissions | Inspect the live EMS and decide Passed/Failed from real observed behavior |
| Help structure test tables, note templates, reports, and compatibility matrices | Capture authentic EMS failure evidence and every compatibility-cell screenshot |
| Help draft a goal-oriented user-test scenario and non-leading probes | Recruit the pilot and 5 real people outside the class; obtain consent and contacts |
| Explain SUS/UEQ-S scoring and calculate scores from authentic student-entered data | Moderate sessions, observe neutrally, and record authentic raw participant data |
| Help cluster genuine findings, review severity reasoning, and improve wording | Submit each genuine finding to Google Form and preserve actual timestamps |
| Help create reusable testing skills and documentation | Verify all AI output, make corrections, maintain Git history, package and submit |
| Help outline the mandatory critique and audit structure | Write an evidence-based critique reflecting the student’s actual experience |

## 14. Prioritized Work Plan

1. **Coordinate scope now:** confirm members, assign one scenario per person, choose ≥3 non-overlapping screens, register personal user accounts where needed, and save the Moodle deadline.
2. **Prepare evidence infrastructure:** establish screenshot/recording naming rules, participant-consent materials, findings-log IDs, and frequent Git commits before live data disappears.
3. **Build Task 1A together:** review lectures/references, log real AI prompts, create >40 items across IA-01–IA-04, add human items, and explain AI omissions.
4. **Pilot Task 2 early:** recruit one extra pilot, test the goal-oriented scenario, measures, SUS/UEQ-S, and probes, then revise the procedure.
5. **Book tools and people:** secure BrowserStack/LambdaTest access and schedule five outside-class participants; these external dependencies are hardest to recover late.
6. **Run live individual work:** execute the checklist on the same ≥3 screens, run five sessions, and capture authentic evidence immediately.
7. **Run compatibility coverage:** cover every required OS/browser/device class per screen, capturing one correctly labelled screenshot for every tested cell.
8. **Report findings twice:** submit each bug/usability improvement to the Google Form as found, then reconcile it with the aggregate log.
9. **Analyse and write:** score authentic SUS/UEQ-S data, calculate metrics, rank findings 0–4, write recommendations, and complete the main report.
10. **Complete compliance and delivery:** finish the audit, 200–300 word critique, disclosure, reusable skills/videos, Git log, PDFs, README self-assessment, archive naming, and final completeness check.
