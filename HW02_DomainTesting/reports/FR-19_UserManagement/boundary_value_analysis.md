# FR-19 Boundary Value Analysis

Rationale: FR-19 has no numeric ranges in the spec, but the target user identifier is an identifier space that benefits from edge-of-space checks. We test the following boundaries: id=0, id=-1 (malformed), smallest existing id in the system, and a very large nonexistent id (999999). These exercise numeric-parsing, validation, and not-found handling.

| TC ID | Precondition | Input | Steps | Expected Result | API Actual Result | Final Status | Notes |
|---|---|---|---|---|---|---|---|
| TC-FR19-BVA-01 | none | DELETE /api/admin/users/0 with admin token | curl DELETE /api/admin/users/0 | 400 Bad Request or 404 Not Found (treat id=0 as invalid/nonexistent) | Not executed (no admin token) | Not executed | Needs admin token to confirm server handling |
| TC-FR19-BVA-02 | none | DELETE /api/admin/users/-1 with admin token | curl DELETE /api/admin/users/-1 | 400 Bad Request (malformed id) | Not executed | Not executed | Requires admin token |
| TC-FR19-BVA-03 | system seeded minimal id observed (smallest existing id) | DELETE /api/admin/users/<smallest-id> with admin token | curl DELETE /api/admin/users/<id> | 403 if id == caller (self-delete) OR 200 if different and permitted | Not executed (admin token missing) | Not executed | Determine smallest existing id from GET /api/admin/users when admin token available |
| TC-FR19-BVA-04 | none | DELETE /api/admin/users/999999 with non-admin token | curl DELETE /api/admin/users/999999 with non-admin bearer | 403 Forbidden (non-admin) OR 404 Not Found if id does not exist | 200 OK {"message":"User deleted"} when executed with non-admin token (observed) | Fail | Demonstrates authorization bypass; server accepted deletion for non-admin bearer. |

Summary of BVA observations:
- We successfully executed a large non-existing id deletion with a non-admin token and observed `200 {"message":"User deleted"}` — this is a critical authorization failure (see bug report).
- Multiple BVA cases remain Not executed because we could not obtain a working admin token in the black-box session; those require admin authentication to verify self-delete rules and id-parsing behavior.
