# Human Review and AI Gaps – Nguyễn Hồng Quân’s Contribution

## Scope and Evidence Boundary

This document covers only the 16 checklist items contributed by **Nguyễn Hồng Quân (22127345)** for **Scenario B – User registers to attend an event**. It does not make claims about another student’s prompts, AI output, corrections, or authorship.

The contribution is verifiable in Git as `week_3/group/EMS_GUI_Checklist_Contribution_02.md` in commit `905bf60` and its parent state before merge commit `3bb402a`. That evidence proves which items Nguyễn Hồng Quân contributed. The original AI response used before the contribution was written is not stored in the repository, so this file does **not** claim that Git proves each item was absent from AI output. The “likely AI gap” column is a retrospective explanation that the student must review and personalise before submission.

## Review Method

1. Recovered the original 16-item contribution from Git history.
2. Mapped original `ADD-*` IDs to the final IDs in `EMS_GUI_Checklist_MASTER.md`.
3. Checked each item against Scenario B screens B1 Home/Events, B2 Event Detail, and B3 Registration Form.
4. Compared each contribution with the group’s earlier checklist categories to explain the additional testing value.
5. Wrote a cautious, item-specific hypothesis about why a generic AI draft could omit that detail. These hypotheses are not presented as verbatim historical facts.

## Contributed Items and Retrospective AI-Gap Analysis

| Final ID | Original ID | What Nguyễn Hồng Quân contributed | Evidence and merge status | Likely AI gap — retrospective hypothesis | Source / EMS characteristic |
| --- | --- | --- | --- | --- | --- |
| GUI-01-02 | ADD-01-001 | Check that labels, statuses, and messages use event-domain language instead of database fields, internal codes, or unexplained technical terms. | Original row is present in commit `905bf60`; retained in the master. | A generic GUI prompt may focus on visual consistency and overlook domain vocabulary or raw API/status text that appears only in real EMS states. | Nielsen #2; Norman Mapping; EMS roles and event/support statuses. |
| GUI-01-03 | ADD-01-002 | Check visual hierarchy, prominence of the primary action, and removal of competing or repeated content. | Original row is present in commit `905bf60`; retained in the master. | AI often produces broad “clean layout” advice without an observable rule such as identifying the page purpose and primary action quickly. | Nielsen #8; Shneiderman #8; responsive B1–B3 layouts. |
| GUI-01-04 | ADD-01-003 | Check affordances for buttons, links, draggable regions, clickable rows, and visibly distinct disabled states. | Original row is present in commit `905bf60`; retained in the master. | Static descriptions of EMS do not reveal which visual elements look interactive or misleading; this requires inspection of the rendered interface. | Norman Affordance/Visibility; Nielsen #6. |
| GUI-01-06 | ADD-01-004 | Check semantic consistency of the same business data across list, detail, form, and export representations. | Original row is present in commit `905bf60`; merged with GUI-01-008 to add date/time/number formatting. | A screen-by-screen AI checklist may not compare one entity across multiple representations and therefore miss cross-screen contradictions. | Nielsen #4; Norman Consistency/Mapping; event dates, slots, roles, and statuses. |
| GUI-02-06 | ADD-02-001 | Check that formats, limits, and examples appear before input and that placeholders do not replace labels or persistent guidance. | Original row is present in commit `905bf60`; retained in the master. | Generic form advice commonly checks whether a placeholder exists but not whether essential instructions disappear when the user begins typing. | Nielsen #5/#6; Norman Visibility/Constraints; dates, Max Slots, email, rich text, and attachments. |
| GUI-02-07 | ADD-02-002 | Check that default values are safe and do not preselect consequential choices such as role, consent, publish, block, or delete. | Original row is present in commit `905bf60`; retained in the master. | AI may treat defaults only as an efficiency feature and fail to distinguish harmless defaults from choices with permission, consent, or destructive consequences. | Nielsen #5; Shneiderman #5; Norman Constraints. |
| GUI-02-08 | ADD-02-003 | Check immediate handling of dependent fields and cross-field rules rather than waiting until submission. | Original row is present in commit `905bf60`; retained in the master. | Without EMS business rules in the prompt, AI may generate isolated field validation but miss relationships such as dates, Max Slots/Waitlist, and role toggles. | Nielsen #5; Norman Constraints/Mapping/Feedback; EMS registration configuration. |
| GUI-02-09 | ADD-02-004 | Check unsaved-change warnings for Back, Cancel, menu navigation, refresh, and closing the tab, including preservation when the user stays. | Original row is present in commit `905bf60`; retained after overlap removal from another item. | A generic checklist may test Cancel or browser Back once but omit the multiple exit paths that can discard a partially completed EMS form. | Nielsen #3; Shneiderman #6; long registration/event/support forms. |
| GUI-03-06 | ADD-03-001 | Check whether functions are grouped and named by user goals rather than the system’s technical structure. | Original row is present in commit `905bf60`; retained in the master. | AI can repeat navigation-consistency rules without evaluating information architecture from the participant’s goal of finding an event, registering, and retrieving a ticket. | Nielsen #2/#6; Norman Mapping; Scenario B journey. |
| GUI-03-07 | ADD-03-002 | Check efficient paths for frequent users without making the novice flow harder. | Original row is present in commit `905bf60`; retained in the master. | A generic output may optimize only learnability or only efficiency instead of checking both novice and experienced-user needs. | Nielsen #7; Shneiderman #2. |
| GUI-03-08 | ADD-03-003 | Check that unauthorized, deleted, expired, or unavailable deep links explain the problem and provide a safe onward route. | Original row is present in commit `905bf60`; merged with GUI-03-008 to add an explicit insufficient-role deep-link check. | Happy-path prompts often omit denied-access and stale-link states; the EMS role model and resettable data make these states especially relevant. | Nielsen #3/#9; Norman Mapping; EMS permissions and periodically reset data. |
| GUI-03-09 | ADD-03-004 | Check web conventions for links versus buttons, disclosure of new tabs/windows, and prevention of resubmission through browser history. | Original row is present in commit `905bf60`; retained in the master. | AI may check whether navigation works but not browser-history side effects such as duplicate registration or repeated submission after Back/Forward. | Nielsen #4; Norman Affordance/Consistency; EMS registration actions. |
| GUI-04-06 | ADD-04-001 | Check duplicate-submit prevention while clearly showing processing state. | Original row is present in commit `905bf60`; expanded in the master with progress/spinner behavior from an overlapping item. | Basic feedback checks often ask only for a spinner or toast and overlook rapid click/Enter repetition creating duplicate records. | Nielsen #5; Norman Feedback/Constraints; Shneiderman #5; registration/support submission. |
| GUI-04-07 | ADD-04-002 | Check toast/banner priority, readability, duration, dismissal, overlap, obstruction, and duplicate messages. | Original row is present in commit `905bf60`; retained while an overlapping toast item was removed. | AI commonly outputs “show a success message” without covering simultaneous notifications, mobile obstruction, reading time, or duplicate events. | Nielsen #3/#8; Shneiderman #1; transient EMS feedback. |
| GUI-04-08 | ADD-04-003 | Check Undo, Restore, or another recovery path where reversal is feasible, rather than relying only on confirmation dialogs. | Original row is present in commit `905bf60`; retained in the master. | Checklist generation often treats confirmation as sufficient error prevention and fails to assess recovery after the user confirms by mistake. | Nielsen #3; Shneiderman #6; cancellation and status changes. |
| GUI-04-09 | ADD-04-004 | Check closure after multi-step flows through a result summary, object identifier/status, and a meaningful next action. | Original row is present in commit `905bf60`; retained in the master. | AI may verify the final button and success toast without checking whether users understand that the whole registration flow is complete and what happens next. | Shneiderman #4; Nielsen #1; Norman Feedback; registration and support workflows. |

## Corrections and Refinements to This Contribution during Group Merge

| Final ID | Change from Nguyễn Hồng Quân’s original contribution | Reason |
| --- | --- | --- |
| GUI-01-06 | Added explicit date/time/number formatting checks from GUI-01-008. | The two items covered overlapping cross-screen consistency risks, so the master retained the broader combined condition. |
| GUI-02-09 | Kept the complete multi-exit unsaved-change test and removed the overlapping clause from another form-structure item. | This preserved one unambiguous item for active navigation away from a dirty form. |
| GUI-03-08 | Added an explicit insufficient-role deep-link test from GUI-03-008. | The merged condition now covers both authorization denial and unavailable resources without duplicate rows. |
| GUI-04-06 | Added progress/spinner behavior while retaining duplicate-submit prevention. | The removed overlapping item contained useful progress-state detail that belonged with the stronger duplicate-action test. |
| GUI-04-07 | Retained the more detailed toast/banner condition and removed the narrower overlapping toast item. | The contribution already covered priority, obstruction, duration, dismissal, and duplicate notifications. |

## Student Verification

- [x] The 16-item contribution and final-ID mapping were recovered from Git, not attributed to another student.
- [x] This document does not describe or judge another student’s prompts or corrections.
- [x] The explanations are item-specific rather than one generic reason repeated for all items.
- [ ] I reviewed each retrospective hypothesis and revised it to match what actually happened during my work.
- [ ] I attached or referenced the original AI output if it is available.
- [ ] If the original AI output is unavailable, I will disclose that limitation rather than claim the table proves an item was absent.
- [ ] Student confirmation — Nguyễn Hồng Quân (22127345), date, and Git commit:
