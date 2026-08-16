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
- **Audit / Correction (student):** _[fill in: did you confirm the lockout logic
  reading against the code yourself? Any part of the breakdown you disagreed with?]_

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
- **Audit / Correction (student):** _[fill in after reviewing the plan file at
  `C:\Users\ACER\.claude\plans\swift-kindling-summit.md` — does the step order and
  the AI/human split match what you actually want to submit?]_

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
- **Audit / Correction (student):** _[fill in: any folder you want renamed/removed,
  any ground rule you disagree with?]_

---

<!-- New entries appended below as each step of the runbook executes. -->
