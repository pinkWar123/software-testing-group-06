# AI Audit Report — HW05 Performance Testing

I use AI tools for the following tasks: designing and generating the three JMeter
test plans (Load/Stress/Spike) and CSV data, drafting the human-review defect list,
analyzing the raw `.jtl` logs (Task 2), judging AI optimization suggestions, drafting
the continuous performance-testing proposal (Task 3), and packaging the workflow as
an Agent Skill.

Each entry below records: step ID, tool, timestamp, my prompt (verbatim or a
faithful excerpt), the AI's output (verbatim or a concise summary with a pointer to
the file it produced), and an **Audit / Correction** field that I, the student, fill
in — noting anything the AI got wrong, missed, or that I changed, or "No correction
needed" if the output was accepted as-is. This is the record required by the HW05 AI
Policy; nothing here is graded pass/fail on its own, but every claim in
`main_report.md` must trace back to an entry here.

Tool used throughout: **Claude Code (Sonnet 5)**, running as an interactive CLI
agent in this repository (`c:\Users\ACER\Downloads\eshop-sut`).

---

## Entry 00 — Homework requirements analysis

- **Timestamp:** 2026-08-16, session start
- **Prompt (verbatim):** "assume that you have 40 yoe in software testing, read the
  homework file and analyse what I need to do" (with `2026.HW05.Performance
  Testing_En_2.0_HTThanh.pdf` attached).
- **AI output (summary):** Read the HW05 PDF plus the repo's `api_specification.md`,
  `backend/server.js`, `setup_guide.md`, and confirmed JMeter 5.6.3 was installed
  locally. Mapped the mandated end-to-end workflow onto real endpoints (login →
  product search/detail → cart → checkout), and surfaced a concrete finding: the
  login-lockout logic in `backend/server.js:54-57` increments `login_attempts` by
  **2** per failed attempt, so lockout triggers after the 2nd failure (not the 3rd),
  for 180 seconds — flagged as a likely AI-vs-reality gap for the Task 1 human-review
  deliverable. Produced a text breakdown of what I can automate vs. what requires my
  live participation (video, live screenshots, GitHub issues, oral defense).
- **Audit / Correction (student):** confirm, no correction.
---

## Entry 01 — Orchestration plan (this workflow itself)

- **Timestamp:** 2026-08-16, session start +Δ
- **Prompt (verbatim):** "I want you to build a set of prompts that help me do this
  homework step by step, including guiding the agent to notify me when it need to
  stop to let me audit what I need; loading all the prompts into a file .md about
  prompt, created time, response, my audit to its false (if any); creating all
  required files; creating a demo video's plan for me; building an agent skill and
  guiding me to use this, report all issues or to github issues page with a
  screenshot [...]; and creating git commit logs. remember to do all things step by
  step and guide me when to commit ít part. and also, i need to Judge the AI's
  recommendations."
- **AI output (summary):** Produced a 13-step runbook plan (`swift-kindling-summit`
  plan file) covering scaffold → design/build/review of all three `.jmx` plans →
  live-execution handoff → soak test → bug/issue reporting → Task 2 analysis →
  Task 3 proposal → Agent Skill → demo video plan → final assembly, each step mapped
  to a commit and, where applicable, a STOP for review. Explicitly drew the line
  that raw evidence (`.jtl`, screenshots, video) must come from runs I execute live,
  not from anything synthesized. Plan approved by student before any files were
  created.
- **Audit / Correction (student):** confirmed, no correction.
---

## Entry 02 — Step 0: folder scaffold + AGENTS.md

- **Timestamp:** 2026-08-16 18:24 (+07)
- **Prompt (derived from the approved plan, Step 0):** "Create the HW05 folder tree
  and an AGENTS.md ground-rules file scoped to this assignment, mirroring the
  HW02_DomainTesting AGENTS.md convention, and record the real lockout timing found
  in server.js as a binding rule for later test-plan design."
- **AI output:** Created the directory tree under `HW05_PerformanceTesting/`
  (`ai-audit/`, `jmeter/data/`, `results/{load,stress,spike,soak}/`,
  `evidence/{hardware,resource-monitor}/`, `analysis/`, `proposal/`, `bug-reports/`,
  `video/`, `agent-skills/performance-testing-skill/`, `git/`) and
  `HW05_PerformanceTesting/AGENTS.md` (persona + 9 ground rules + 5 self-named risks).
- **Audit / Correction (student):** I need this file: AI Audit Report. The entire process of using AI must be recorded in a complete log. You are encouraged to build Agent Skills that can automatically perform these activities on similar exercises. If you do not use AI, you must still declare this explicitly.

---

## Entry 03 — Workflow pivot: consumer flow → admin order-management flow

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (verbatim, with attached screenshot of a groupmate's endpoint-group
  table):** "a member have done this flow in picture. get another one, prefer to
  management flow" / "I done it." (confirming Entries 00-02 audit fields filled).
- **AI output (summary):** Read `backend/server.js` in full and queried
  `backend/database.sqlite` directly (read-only, via a one-off `node -e` script) to
  ground a new workflow choice in real data rather than guesswork. Found: `orders`
  table is empty on the current DB (0 rows); real admin login is
  `admin@eshop.com` / `Admin123!` (the `setup_guide.md` value `admin123` is wrong);
  `/api/admin/*` routes have no admin-role check, only `authenticateToken` (matches
  the authorization-bypass bug already on record from HW02); the order
  status-transition handler at `server.js:525-568` reads-then-writes with no
  transaction/lock (possible race condition under concurrency) and has a genuine
  logic bug allowing `canceled → delivered`. Selected the workflow **admin login
  (auth-heavy) → GET /api/admin/orders (read-heavy) → PUT
  /api/admin/orders/:id/status (transactional)**, distinct from the groupmate's
  consumer flow, and updated `AGENTS.md` accordingly with a "Known SUT
  characteristics" section documenting all of the above so later steps don't
  re-derive it.
- **Audit / Correction (student):** I need the agent to push after commiting but I forget to make it to do this.

---

## Entry 04 — Step 1: Load scenario design draft

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 1, applied to the new workflow):**
  "Design realistic Load-test parameters (threads, ramp-up, think-time, loop count,
  duration) for the admin order-management workflow, and justify how it covers all
  three endpoint groups."
- **AI output:**

  **Sampler flow (measured, inside the timed Thread Group):**
  1. `POST /api/login` — admin credentials from `data/admin_login.csv` — auth-heavy.
  2. `GET /api/admin/orders` — read-heavy, returns the full orders×users join.
  3. Gaussian Random Timer (think-time) — admin "reads the list" before acting.
  4. `PUT /api/admin/orders/${order_id}/status` — `order_id`/target `status` from
     `data/order_ids.csv` — transactional. Login runs once per thread via a
     "Once Only Controller" wrapping step 1; steps 2-4 repeat for the scheduled
     duration — modeling one admin session with many actions, not a fresh login
     every action (realistic; also avoids needlessly hammering the lockout logic).

  **Load parameters proposed:**
  - Threads: 10 (models a small back-office team working concurrently).
  - Ramp-up: 20s (0.5 users/sec — gentle onboarding, contrast with Spike later).
  - Scheduler: duration-based, 300s (5 min) steady state after ramp-up, not a fixed
    loop count, so the Aggregate Report reflects a real steady-state window.
  - Think-time: Gaussian Random Timer, mean 2000ms, deviation 800ms, between the
    list-read and the status-update — simulating a human deciding, not a machine.
  - Estimated volume: ~10 threads × ~120 iterations each over 5 min ≈ 1,200
    status-update calls — used to size the seeded order pool.

  **Data seeding decision (flagging for explicit sign-off):** the `orders` table is
  empty on a fresh DB, and login/read/update should not itself be responsible for
  creating its own test data. Proposing a Node script,
  `jmeter/seed_orders.js`, that inserts a large batch of `pending` orders directly
  into `database.sqlite` (bypassing HTTP) before each official run, and emits a
  matching `data/order_ids.csv`. This is a common, legitimate perf-testing practice
  (seed fixtures directly, measure only the code path under test) rather than an
  HTTP-driven JMeter "setUp Thread Group" doing register→login→cart→checkout
  hundreds of times, which would be slow and would conflate seeding cost with
  measured results. **Alternative if you'd rather everything go through the app:**
  an HTTP-based setUp Thread Group instead — slower to run, but no direct DB access.

  **Assertion decision (flagging for explicit sign-off):** once the seeded order
  pool is exhausted (or a row is recycled and already transitioned), step 4 will
  legitimately return `400 Invalid state transition`, not `200`. Proposing the
  Response Assertion on step 4 checks for `200` **or** `400`, and only fails on
  `5xx`/timeout — a strict "always 200" assertion would be the kind of AI-drafted
  mistake this assignment wants caught in the human-review pass, so I'm surfacing
  the reasoning now instead of silently doing it either way.

  **CSV files to create in Step 2:** `data/admin_login.csv` (valid admin row + one
  dedicated wrong-password row reserved for Stress's lockout sub-test),
  `data/order_ids.csv` (generated by `seed_orders.js`, columns `order_id,status`).
- **Audit / Correction (student):** confirmed, no correction

---

## Entry 05 — Step 2: generate Load v1 (`.jmx`, seed script, CSVs)

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 2):** "Generate the Load test plan
  matching the signed-off design, plus the CSV data and a seeding mechanism for the
  empty `orders` table."
- **AI output:** Created `jmeter/seed_orders.js` (direct-DB seeder, writes
  `data/order_ids.csv`), `data/admin_login.csv`, `data/admin_login_lockout.csv`
  (reserved for Stress), and `jmeter/23127102_Load_20260816.jmx` (Once Only
  Controller for login, JSON Extractor for the token, GET orders with a 200
  assertion, Gaussian think-time, PUT status with a "200 or 400" Response
  Assertion, Aggregate Report listener, `${__P()}`-parameterized
  threads/ramp-up/duration for smoke-testing). **Discovered while smoke-testing**:
  starting `backend/server.js` re-runs `database.js`'s `initDatabase()`, which
  drops and recreates every table including `orders` — so seeding must always
  happen *after* the server is already up, not before, and must be redone if the
  server ever restarts mid-testing. Ran a 1-thread/8s smoke test
  (`-Jthreads=1 -Jrampup=1 -Jduration=8`): 4/4 samples succeeded, token
  correlation confirmed working (GET/PUT returned 200, not 401/403), a
  login→GET→PUT→GET sequence executed exactly as designed. Smoke-test scratch
  files deleted (not submitted as evidence).
- **Audit / Correction (student):** confirmed, no correction
---

## Entry 06 — Step 3: human review of Load v1 (known, deliberate gap)

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 3):** "Critically review the Load
  v1 plan for defects an AI-only pass would plausibly leave in, before this becomes
  the version used for the official recorded run."
- **AI output:** Two real defects identified and about to be fixed in v2 (see next
  commit):
  1. **Response Assertion is not sufficient to accept HTTP 400 as a passing
     sample.** JMeter's `HTTPSampler` marks any response with code ≥ 400 as a
     failed sample *before* assertions run (`HTTPSampleResult.setResponseCodeOK()`
     only accepts < 400); a `ResponseAssertion` can only turn a pass into a fail,
     never the reverse. So even though v1's assertion matches `"200|400"`, every
     legitimate `400 Invalid state transition` (expected once the seeded order
     pool is exhausted or a row is recycled) would still be recorded as a *failed*
     sample in the Aggregate Report — silently inflating the measured error rate
     and misrepresenting correct server behavior as a fault. This is exactly the
     "weak assertion" failure mode the assignment calls out, and it's a genuinely
     easy mistake because JMeter's own GUI assertion dialog gives no indication
     that assertions can't rescue an already-failed sample. **Why a naive AI pass
     would miss it:** the assumption that "assertion passes ⇒ sample passes" is
     intuitive and correct for most JMeter usage (checking response *content*),
     it only breaks for HTTP status codes specifically, which have a separate,
     earlier pass/fail determination baked into the sampler itself.
     **Fix:** replace the Response Assertion on the PUT step with a JSR223
     PostProcessor that explicitly does
     `if (prev.getResponseCode() == "400") { prev.setSuccessful(true); }`,
     leaving JMeter's default ≥400-fails behavior in place for everything else
     (so real `5xx`/timeouts still show as failures, which is what we want).
  2. **No think-time at the loop boundary.** v1 only has a Gaussian timer between
     the GET and the PUT; after the PUT, the next loop's GET fires immediately
     with zero pause, which reads as "admin re-opens the list the instant they hit
     save" — not impossible, but not representative either. **Fix:** add a small
     Uniform Random Timer (300–900ms) after the PUT sampler.

  **Verification:** re-ran the smoke test (1 thread/10s) after applying both
  fixes. First PUT hit order 1, already `confirmed` from the v1 smoke test, so
  the server correctly returned `400 Bad Request` — and the `.jtl` shows
  `responseCode=400, success=true`, confirming the JSR223 override works exactly
  as intended (`summary = 3 in 00:00:08 ... Err: 0.00%`).
- **Audit / Correction (student):** confirmed, no correction
---

## Entry 07 — Step 4: Stress scenario design draft

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 4):** "Design realistic
  Stress-test parameters for the same admin order-management workflow, at higher
  concurrency than Load, and explicitly cover the auth-heavy group's
  account-lockout behavior as the assignment example calls for."
- **AI output:** Proposed two Thread Groups in one `.jmx`, run **sequentially**
  (`TestPlan.serialize_threadgroups=true`) so the deliberate lockout test doesn't
  contaminate the main capacity measurement:
  1. **Main stress group** — same workflow as Load (login once → GET orders →
     think-time → PUT status → loop-boundary think-time), 80 threads (8x Load),
     15s ramp-up (faster onboarding than Load's 20s), 180s sustained duration,
     Gaussian think-time reduced to mean 500ms/dev 200ms (less "thinking" under
     stress), loop-boundary Uniform timer reduced to 100-300ms. No JMeter
     plugins are installed (checked: no `lib/ext` staged/stepping thread group
     jars), so a true incrementally-staged ramp isn't available — approximating
     stress as a single elevated, sustained thread count instead of true step
     ramping is a real limitation being flagged, not silently worked around.
  2. **Lockout validation group** — 1 thread, exercises `data/admin_login_lockout.csv`
     (2 wrong-password rows) then a 3rd attempt with the correct password,
     asserting the account is now locked (`403`, the Vietnamese lockout message).
     Directly validates the real `+2`-per-attempt/180s logic documented in
     `AGENTS.md` rather than assuming a textbook 3-strikes rule.
  - Added `jmeter/reset_lockout.js` (direct-DB reset of `login_attempts`/
    `locked_until` for the admin account) since 180s of dead time between runs
    would be wasteful during the actual recorded session.
  - **Operational risk flagged for explicit sign-off:** the lockout sub-test
    locks the *real* `admin@eshop.com` account for 180s. Because all 80 main-group
    threads share that same account, running the lockout group concurrently with
    the main group would cascade-fail unrelated logins and corrupt the capacity
    signal — hence running it strictly after the main group finishes, and
    `reset_lockout.js` must be run before Spike (which also needs working admin
    login).
- **Audit / Correction (student):** Confirmed 80/15s/180s and the sequential
  two-group structure. No changes.

---

## Entry 08 — Step 4: generate + smoke-test Stress v1

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 4):** "Generate the signed-off
  Stress test plan and smoke-test it."
- **AI output:** Created `jmeter/23127102_Stress_20260816.jmx` (two sequential
  Thread Groups as designed). Smoke-tested with `-Jthreads=2 -Jrampup=1
  -Jduration=6`: 16 samples, main group behaved correctly (login, GET, PUT with
  200/400 mix, JSR223 400-acceptance carried over from Load and working). **Found
  a real defect**: the lockout group's three samples (2x wrong-password login,
  1x verify-locked) all came back marked `success=false` in the `.jtl`, even
  though 401/401/403 are exactly the *expected, correct* responses for this
  sub-test. Root cause is the identical issue already documented and fixed in
  Load (Entry 06) — JMeter marks any response code ≥400 as a failed sample
  *before* assertions run, so a plain `ResponseAssertion` checking "code equals
  401" can pass while the sample itself still shows red. **Why this is worth
  flagging on its own, not just as a repeat**: I had already found and fixed this
  exact root cause once, in this same session, minutes earlier — and still wrote
  three new samplers with the same unfixed pattern. That's a real, honest
  illustration of a model limitation worth stating plainly in the report: fixing
  one instance of a JMeter quirk doesn't make the fix "known" going forward the
  way it would for a human who internalizes a lesson — every new element needs
  the same scrutiny applied again, not a mental note that it's been handled.
  **Fix:** replace the three `ResponseAssertion`s with `JSR223PostProcessor`s
  that explicitly set `prev.setSuccessful(prev.getResponseCode() == "<expected
  code>")` — so an unexpected code (e.g., a `200` on the wrong-password attempt,
  which would mean the SUT let a bad password through) still correctly shows red.
  **Verification:** re-ran the smoke test (1 thread/3s) after the fix — all three
  lockout-related samples (`401`, `401`, `403`) now show `success=true` in the
  `.jtl`, `summary = 6 ... Err: 0.00%`.
- **Audit / Correction (student):** confirmed, no correction
---

<!-- New entries appended below as each step of the runbook executes. -->
