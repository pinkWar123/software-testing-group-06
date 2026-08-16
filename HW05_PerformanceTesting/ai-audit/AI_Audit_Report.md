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
- **Audit / Correction (student):** _[fill in: confirm this doesn't overlap a
  different groupmate's admin-side pick; confirm the admin credentials work on your
  running instance.]_

---

## Entry 04 — Step 1: Load scenario design draft

- **Timestamp:** 2026-08-16 (session continued)
- **Prompt (derived from the approved plan, Step 1, applied to the new workflow):**
  "Design realistic Load-test parameters (threads, ramp-up, think-time, loop count,
  duration) for the admin order-management workflow, and justify how it covers all
  three endpoint groups."
- **AI output:** See the design proposal below (posted to chat for your sign-off
  before any `.jmx` or CSV is generated, per the runbook's Step 1 STOP).
- **Audit / Correction (student):** _[pending — fill in after reviewing the design
  message]_

---

<!-- New entries appended below as each step of the runbook executes. -->
