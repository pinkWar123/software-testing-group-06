# Screenshot / Evidence Inventory — HW05

Tracks every piece of visual evidence required by the assignment so nothing is
requested twice and nothing required is missed at submission time.

| ID | Scenario | Type | What it must show | File path | Status |
|----|----------|------|--------------------|-----------|--------|
| E-001 | Load | Tool + resource monitor | JMeter (running) + Task Manager Details tab (node.exe CPU/mem) in the same frame | `evidence/resource-monitor/load.png` | Captured |
| E-002 | Stress | Tool + resource monitor | Same, during Stress run | `evidence/resource-monitor/stress.png` | Captured |
| E-003 | Spike | Tool + resource monitor | Same, during Spike run | `evidence/resource-monitor/spike.png` | Captured |
| E-004 | Soak | Tool + resource monitor | Same, during the 10-15 min endurance run (take 2-3 samples across the run) | `evidence/resource-monitor/soak_*.png` | Skipped (student decision, 2026-08-16) |
| E-005 | Hardware | dxdiag | Full dxdiag output, hostname visible and matching prior HW deployments | `evidence/hardware/dxdiag.png` | Captured |
| E-006 | Hardware | Spec table | CPU / RAM / OS / Node version summarized in `evidence/hardware/spec_table.md` | `evidence/hardware/spec_table.md` | Confirmed |
| E-007 | Load | HTML report | `jmeter -e -o` generated report folder | `results/load/html-report/` | Confirmed |
| E-008 | Stress | HTML report | Same | `results/stress/html-report/` | Confirmed |
| E-009 | Spike | HTML report | Same | `results/spike/html-report/` | Confirmed |
| E-010 | Soak | HTML report | Same | `results/soak/html-report/` | Skipped (student decision, 2026-08-16) |
| E-011 | Bugs | Bug screenshots | One screenshot per bug filed in `bug-reports/bug_report.md` / GitHub Issues | `bug-reports/screenshots/` | Confirmed |
| E-012 | Video | Demo video | ≥6 min, tool + monitor in frame, own Vietnamese narration, unlisted YouTube link | https://youtu.be/w4NyDbQaXLM | Confirmed |

Status values: `Pending` (not captured yet) → `Captured` (file exists, not yet
reviewed) → `Confirmed` (student has reviewed the file and it's correct).
