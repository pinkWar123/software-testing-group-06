# HW05 — Performance Testing — README

Student: **23127102** | SUT: EShop backend (`http://localhost:3000`) | Branch:
`week_5/23127102`

## Workflow under test

**Admin order-management** (chosen instead of the consumer login→search→
cart→checkout flow to avoid duplicating a groupmate's pick):

`POST /api/login` (admin, auth-heavy) → `GET /api/admin/orders` (read-heavy)
→ `PUT /api/admin/orders/:id/status` (transactional). Full rationale and the
real SUT findings behind this choice are in `AGENTS.md` and
`ai-audit/AI_Audit_Report.md` (Entry 03).

## Test summary report

| Item | Result |
|---|---|
| Scenarios run | **Load** ✅, **Stress** ✅, **Spike** ✅. **Soak/endurance** ❌ — not run (student decision after Load/Stress/Spike were complete; see note below). |
| Endpoint groups covered | Auth-heavy (`POST /api/login`, incl. account-lockout validation in Stress), Read-heavy (`GET /api/admin/orders`), Transactional (`PUT /api/admin/orders/:id/status`) — same workflow across all three executed scenarios. |
| Endurance threshold | **Not determined** — the soak test that produces this number was skipped. This is a known, acknowledged gap against the assignment's requirement to "determine the endurance threshold" — see note below. |
| Samples collected | Load: 1,115 · Stress: 6,465 · Spike: 2,210 (raw `.jtl` in `results/`) |
| Bugs / issues found | 1 — **BUG-HW05-001**: `PUT /api/admin/orders/:id/status` incorrectly accepts a `canceled → delivered` transition (`backend/server.js:550-551`). Reproduced with curl evidence in `bug-reports/bug_report.md`. Not yet filed as a GitHub issue (needs a screenshot + explicit go-ahead). No genuine performance issues (elevated error rate) were found — error rate was 0% (by design; see `analysis/misinterpretation_hunt.md` #1) in all three runs. |
| Demo video | <https://youtu.be/w4NyDbQaXLM> (unlisted) |

**Note on the skipped soak test:** the assignment requires "a short endurance
test (~10-15 min) to empirically find your hardware's threshold, reported
with concrete numbers." The plan and runbook for it exist
(`jmeter/23127102_Soak_20260816.jmx`, `EXECUTION_RUNBOOK.md` §6) and it was
smoke-tested successfully, but the official run was not executed — this is a
real, acknowledged gap in the submission, not an oversight being hidden. The
Stress/Spike data still supports a partial, indirect read: Stress (80
threads, sustained 180s) held a 0% error rate throughout at ~1.4s average
latency, suggesting the backend *survives* sustained load at that
concurrency without crashing, even though it doesn't *perform well* there —
but this is not a substitute for the soak test's actual purpose (detecting
drift/leaks over time) and shouldn't be reported as one.

## Deliverables map

| Deliverable | Location |
|---|---|
| Main report | `main_report.md` |
| Test plans | `jmeter/23127102_{Load,Stress,Spike,Soak}_20260816.jmx` |
| CSV data | `jmeter/data/` |
| Raw `.jtl` logs + HTML reports | `results/{load,stress,spike}/` |
| Resource-monitor / hardware evidence | `evidence/` |
| AI Audit Report | `ai-audit/AI_Audit_Report.md` |
| AI Critique | `ai-audit/AI_Critique.md` |
| Task 2 analysis | `analysis/` |
| Task 3 proposal | `proposal/continuous_performance_testing.md` |
| Agent Skill | `agent-skills/performance-testing-skill/SKILL.md` (also live at `.claude/skills/`) |
| Bug report | `bug-reports/bug_report.md` |
| Demo video plan | `video/demo_video_plan.md` |
| Git commit log | `git/commit_log.txt` |

## Self-assessment

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | Task 1 — Load testing | 20 | _(fill in)_ |
| 2 | Task 1 — Stress testing | 20 | _(fill in)_ |
| 3 | Task 1 — Spike testing | 20 | _(fill in)_ |
| 4 | Task 2 — AI analysis + misinterpretation hunt | 10 | _(fill in)_ |
| 5 | Task 3 — Continuous Performance Testing proposal (G9.6) | 10 | _(fill in)_ |
| 6 | Agent Skills | 10 | _(fill in)_ |
| | **Total** | **100** | _(fill in)_ |

The "Self-Assessed Grade" column is your own declaration for the submission
filename (`23127102_HW05_AI_Performance_<grade>.zip`) — deliberately left for
you to fill in rather than self-graded here; you're best placed to weigh the
soak-test gap above against everything else that's complete.
