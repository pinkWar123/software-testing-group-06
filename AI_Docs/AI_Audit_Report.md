# AI Audit Report — Scenario C (Admin manages users)

---

### Log Entry 1

- **AI Tool:** Claude Pro (VS Code)
- **Timestamp:** 2026-08-04 22:47:05
- **User Prompt:** "Here is the input for screen C1. The screenshot reference is images/C1_UsersList.png. Please execute the WORKFLOW from your Agent Skill to generate the evaluation table. Remember to append the table to Task1_GUI/Task1B_Checklist.md and log the interaction in AI_Docs/AI_Audit_Report.md automatically"
- **AI Output Summary:** Evaluated all 48 checklist items against C1 - Users List (`images/C1_UsersList.png`). Result: 10 Passed, 4 Failed, 34 N/A (mostly flagged [REQUIRES HUMAN VERIFICATION] due to missing states/screens — empty list, mobile viewport, dialogs, other screens for cross-consistency, or DOM-only attributes). Failed IDs: GUI-01-03 (Export/Add User buttons compete visually), GUI-02-02 (search input lacks visible persistent label), GUI-02-06 ("Go to page" input lacks range hint), GUI-03-11 (Role/Status filter icons lack visible label). Results appended to `Task1_GUI/Task1B_Checklist.md`.

---

### Log Entry 2

- **AI Tool:** Claude Pro (VS Code)
- **Timestamp:** 2026-08-04 22:53:58
- **User Prompt:** "Here is the input for screen C2. The screenshot reference is images/C2_EditUser.png. Please execute the WORKFLOW from your Agent Skill to generate the evaluation table. Remember to append the table to Task1_GUI/Task1B_Checklist.md and log the interaction in AI_Docs/AI_Audit_Report.md automatically"
- **AI Output Summary:** Evaluated all 48 checklist items against C2 - Edit User modal (`images/C2_EditUser.png`), cross-referenced against C1 for the same user record (email 123123123@gmail.com). Result: 12 Passed, 4 Failed, 32 N/A. Failed IDs: GUI-01-06 (First/Last Name values appear swapped between the C1 list and the C2 edit form for the same record), GUI-02-01 (no required-field marking convention; Phone Number's requirement status is ambiguous), GUI-02-06 (Phone Number placeholder repeats the label instead of showing a format example), GUI-02-11 (Member Code's "Optional" status only exists as placeholder text, not a persistent marker). Results appended to `Task1_GUI/Task1B_Checklist.md`.

---

### Log Entry 3

- **AI Tool:** Claude Pro (VS Code)
- **Timestamp:** 2026-08-04 22:58:08
- **User Prompt:** "Here is the input for screen C1. The screenshot references are images/C4_ExcelExport_1.png and C4_ExcelExport_2.png (the screen of file excel). Please execute the WORKFLOW from your Agent Skill to generate the evaluation table. Remember to append the table to Task1_GUI/Task1B_Checklist.md and log the interaction in AI_Docs/AI_Audit_Report.md automatically" (note: prompt labeled the screen "C1" but the referenced images/content are for the Excel Export action — logged as screen C4 per the filenames provided)
- **AI Output Summary:** Evaluated all 48 checklist items against C4 - Excel Export, covering both the browser download toast (`images/C4_ExcelExport_1.png`) and the opened export file (`images/C4_ExcelExport_2.png`). Result: 4 Passed, 3 Failed, 41 N/A. Failed IDs: GUI-01-02 (downloaded filename exposes a raw internal timestamp/ID), GUI-01-06 (field naming diverges between web UI and export — "Member Code"/"Card Code", "Phone Number"/"Phone", missing "Updated" column, and the same admin's name renders in a different word order between the C1 list and the export header), GUI-01-07 (Status values in the export are untranslated Vietnamese despite English column headers and an English-mode UI). Results appended to `Task1_GUI/Task1B_Checklist.md`.

---
