# Bug / Performance Issue Reports — HW05

Found while designing and reviewing the performance test plans (not from load
data — this one is a functional logic bug, reproducible with a single request).
Additional entries will be appended here as they're found during the official
Load/Stress/Spike/Soak runs (error responses, crashes, elevated latency, etc.).

---

## BUG-HW05-001 — Order status machine accepts `canceled → delivered`

**Severity:** Medium (data-integrity / business-logic correctness)
**Component:** `PUT /api/admin/orders/:id/status`
**Location:** [backend/server.js:550-551](../../backend/server.js#L550-L551)

**Description:** The order state machine's transition table has an explicit,
intentional-looking exception that allows a `canceled` order to be marked
`delivered`:

```js
if (currentStatus === "canceled" && status === "delivered")
  isValidTransition = true;
```

Every other transition in the same function follows a sensible forward-only
state machine (`pending → confirmed/canceled`, `confirmed → shipping/canceled`,
`shipping → delivered`). This one line lets a canceled order — which should be
terminal — jump straight to `delivered`, which doesn't correspond to any real
fulfillment event (nothing was ever shipped) and would corrupt order-history
reporting and any downstream logic that assumes `delivered` implies the order
was actually shipped.

**Steps to reproduce:**
1. Log in as admin: `POST /api/login` with `admin@eshop.com` / `Admin123!`.
2. Create/seed an order with `status = 'canceled'` (id `1` used below).
3. `PUT /api/admin/orders/1/status` with body `{"status":"delivered"}`.

**Evidence (curl, reproduced 2026-08-16 against a freshly-seeded local
instance):**
```
$ curl -X PUT http://localhost:3000/api/admin/orders/1/status \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <admin token>" \
    -d '{"status":"delivered"}'
{"message":"Order status updated"}

$ curl http://localhost:3000/api/admin/orders -H "Authorization: Bearer <admin token>"
[{"id":1,...,"status":"delivered",...}]
```
Expected: `400 {"error":"Invalid state transition from canceled to delivered"}`
(consistent with every other invalid transition the same endpoint correctly
rejects). Actual: `200`, transition accepted.

**Screenshot:** _[to attach — a Postman/browser screenshot of the same request,
or a screen-recorded terminal capture, before filing as a GitHub issue]_

**Related:** `/api/admin/*` routes (including this one) only check
`authenticateToken`, not an admin role (`backend/server.js:494-568` — no
`isAdmin` middleware), so any authenticated user can currently trigger this,
not just admins. This matches the authorization-bypass finding already on
record in `HW02_DomainTesting/bug-reports/bug_report.md`.

**GitHub issue:** not yet filed — draft ready, filing requires your
confirmation (per `AGENTS.md` ground rule: GitHub issues are never posted
without asking each time). Say the word and I'll open it.

---

## Performance issues (from Load/Stress/Spike/Soak runs)

_To be appended once the official runs in `EXECUTION_RUNBOOK.md` are complete.
Logging performance issues (elevated latency, error rate) is encouraged by the
assignment but not penalized if none are found._
