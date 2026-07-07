# FR-19 Domain Testing

Summary: Domain testing for Feature FR-19 (User Management - Admin). Tests follow the assignment's dual-channel rule: UI evidence (screenshots) + independent API curl checks. Where a UI path exists, both channels are required; if the API disagrees with a passing UI the TC is FAIL overall.

Table of Domain Test Cases

| TC ID | Precondition | Input / Action | Steps (UI/API) | Expected Result | UI Actual Result | API Actual Result (status + body summary) | Final Status | Covered EP classes |
|---|---|---|---|---|---|---|---|---|
| TC-FR19-01 | none | GET /api/admin/users with NO token | API: curl GET /api/admin/users without Authorization | 401 Unauthorized | n/a (no UI path) | 401 {"error":"Unauthorized"} | Pass | Caller role = no token (invalid) |
| TC-FR19-02 | none | GET /api/admin/users with invalid token | API: curl GET /api/admin/users with malformed/invalid bearer | 403 Forbidden | n/a | 403 {"error":"Forbidden"} | Pass | Caller role = invalid token (invalid) |
| TC-FR19-03 | register and login as non-admin user (bbtest_nonadmin@eshop.com) | GET /api/admin/users with non-admin token | API: curl GET /api/admin/users with non-admin bearer; UI: (no UI control surface for non-admin) | 403 Forbidden (server must enforce admin-only) | n/a | 200 OK — returned JSON array of users (example: [{"id":3,"name":"BB Test User",...}, ...]) | Fail (Authorization bypass) | Caller role = non-admin token (invalid) |
| TC-FR19-04 | register and login as non-admin user | DELETE /api/admin/users/:id (existing) with non-admin token | API: curl DELETE /api/admin/users/999999 with non-admin bearer | 403 Forbidden | n/a | 200 OK {"message":"User deleted"} | Fail (Authorization bypass — deletion allowed) | Caller role = non-admin token; Target id exists/does-not-exist |
| TC-FR19-05 | admin UI logged in (expected: admin@eshop.com) | UI view: open Admin → Người dùng page | UI steps: Open http://localhost:5174 and navigate to "Người dùng" while logged in as admin | UI: full user list shown, no password columns; delete controls visible on rows | UI screenshot: S-001 shows IDs/emails/roles and "Xóa" buttons; no password visible in UI | API: Not executed with admin token (admin login unsuccessful in black-box run); separate API checks showed non-admin tokens were accepted — mismatch risk; without an admin token cannot confirm server-side enforcement | Not fully executed — Needs admin API verification | Caller role = admin token (valid) |
| TC-FR19-06 | Admin self-delete attempt (DELETE /api/admin/users/:id where id == caller) | Attempt to delete own account via API and via UI (if UI provides control) | UI: attempt to delete logged-in admin row; API: curl DELETE /api/admin/users/<admin id> with admin bearer | Expected: UI blocks or hides self-delete; API must reject (403) | UI: (per screenshots, delete control presence for admin row unclear in some images; see S-002) | API: Not executed (no admin token available); cannot confirm | Not executed — needs admin credentials | Target user id = exists and IS caller (invalid — self-deletion) |

Notes:
- UI screenshots were provided by the tester and are logged as S-001..S-003 in `evidence/screenshot_inventory.md`.
- API evidence collected during black-box checks shows important failures: non-admin bearer tokens were able to GET the admin users list (200) and DELETE (200) — these are authorization/AC failures and are reported as bugs.
- Login responses observed in earlier API runs also returned a `user` object containing a `password` field for newly created accounts (data exposure); that is a separate critical bug and is recorded in the bug report.

Execution status: partial — Non-admin auth misuse and deletion acceptance confirmed via API; admin-token checks not completed due to inability to obtain the seeded admin token during black-box run. Next step: file bug reports and update BVA tests.
