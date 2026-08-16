# Execution Runbook — Load / Stress / Spike / Soak

This is Step 6 (+7) of the HW05 runbook: everything is designed, built, smoke-tested
and committed (see `ai-audit/AI_Audit_Report.md`, Entries 04-10). What's left needs
**you**, live — this produces the graded raw evidence (`.jtl`, HTML reports,
resource-monitor screenshots, hardware report, demo video). Nothing in this document
is optional filler; every step maps to a required deliverable.

Work through this once, top to bottom. Tick items off as you go (mentally or in
`evidence/screenshot_inventory.md`, which already has a row for each screenshot).

## 0. One-time setup (before the first recorded run)

1. Close unnecessary apps — the hardware snapshot in
   `evidence/hardware/spec_table.md` shows only ~2 GB free out of 16 GB, which will
   distort the soak test's "memory ceiling" finding if left as-is.
2. Open **Task Manager → Details tab**, add/sort by CPU and Memory columns, and
   locate the `node.exe` process (the backend) — you'll want it visible throughout.
3. Set up your screen recorder so **the JMeter/terminal window and Task Manager are
   both visible in the same frame** — this is a hard requirement for the demo video
   and for each run's resource-monitor screenshot.
4. Run `dxdiag`, screenshot the summary, save as `evidence/hardware/dxdiag.png`.
5. All commands below assume your terminal's working directory is
   `HW05_PerformanceTesting/jmeter/`.

## 1. Starting the backend (do this fresh before EVERY scenario)

```
cd path/to/eshop-sut/backend
node server.js
```

**Important, confirmed during smoke-testing (Entry 05):** starting the server
re-runs `database.js`'s `initDatabase()`, which **drops and recreates every
table**, wiping any previously seeded orders and resetting `orders` to empty. So
the sequence for every official run is always: **start server → seed orders →
run JMeter** — never seed before starting the server, and re-seed if the server
ever restarts mid-testing.

## 2. Seeding orders (fresh before EVERY official run)

From `HW05_PerformanceTesting/jmeter/`, with the backend already running:

```
node seed_orders.js <count>
```

Suggested counts (generous, so most requests get a real `200` rather than a
recycled `400` — both are handled correctly, but a healthy mix is more
representative):

| Scenario | Suggested seed count | Why |
|---|---|---|
| Load | 2,000 | ~1,200 estimated PUT calls over 5 min at 10 threads |
| Stress | 10,000 | 80 threads × 180s at a faster pace — many more iterations |
| Spike | 5,000 | Baseline + 150-thread burst + recovery |
| Soak | 8,000–15,000 | 12 min sustained — size to your chosen thread count (see §6) |

## 3. Running each scenario (headless — see the GUI-mode note in §7)

General form:

```
jmeter -n -t 23127102_<Scenario>_20260816.jmx ^
  -l ..\results\<scenario>\<scenario>.jtl ^
  -e -o ..\results\<scenario>\html-report
```

(Use `\` continuation or put it on one line in PowerShell/CMD — the `^` line
continuation above is for `cmd.exe`; in PowerShell just put it on one line or use
`` ` ``.) The `-e -o` flags generate the HTML report folder automatically.

### Load
```
jmeter -n -t 23127102_Load_20260816.jmx -l ..\results\load\load.jtl -e -o ..\results\load\html-report
```
Runs ~5 min 20s (20s ramp-up + 300s duration). Defaults (10 threads/20s ramp/300s)
are already the signed-off values — no `-J` overrides needed for the official run.

### Stress
```
jmeter -n -t 23127102_Stress_20260816.jmx -l ..\results\stress\stress.jtl -e -o ..\results\stress\html-report
```
Runs ~3 min 15s main group + a few seconds for the lockout group. **This
deliberately locks the real admin account for 180s at the end** (that's the
point — it's validating the real lockout logic). After it finishes:
```
node reset_lockout.js
```
before doing anything else that needs admin login (including Spike).

### Spike
```
jmeter -n -t 23127102_Spike_20260816.jmx -l ..\results\spike\spike.jtl -e -o ..\results\spike\html-report
```
Runs ~30s baseline + ~30s burst + ~30s recovery (~1.5 min total). Confirm the
admin account isn't still locked from Stress before starting (run
`node reset_lockout.js` if unsure — it's a no-op/harmless if already unlocked).

## 4. What to capture during each run

For each of Load/Stress/Spike (and Soak), while it's running:
- **1 screenshot**: JMeter/terminal output + Task Manager (`node.exe` row visible)
  in the same frame → save to `evidence/resource-monitor/<scenario>.png`.
- Let it finish. Confirm `results/<scenario>/<scenario>.jtl` has rows and
  `results/<scenario>/html-report/index.html` was generated.
- Update `evidence/screenshot_inventory.md`: mark the corresponding row
  `Captured`, and `Confirmed` once you've looked at the file.

## 5. Between Stress and Spike specifically

1. `node reset_lockout.js` (undo the deliberate lockout from Stress).
2. Re-seed orders for Spike (§2).
3. Confirm with a quick manual login check if you want extra certainty:
   `curl -X POST http://localhost:3000/api/login -H "Content-Type: application/json" -d "{\"email\":\"admin@eshop.com\",\"password\":\"Admin123!\"}"`
   should return a `token`, not a 403.

## 6. Soak / endurance test

Purpose: not to find the breaking point (Stress already does that) but to prove a
chosen load level is **sustainable over time** — 12 minutes, not 3.

1. Look at your actual Stress results first. Pick a thread count that Stress
   showed as comfortably healthy (low error rate, stable latency) — this is a
   judgment call you make from real data, not a number I can pick in advance.
   The plan defaults to 25; override if your Stress data suggests otherwise:
   ```
   jmeter -n -t 23127102_Soak_20260816.jmx -l ..\results\soak\soak.jtl -e -o ..\results\soak\html-report -Jthreads=<N>
   ```
2. Seed generously first (§2 table) — at `<N>` threads for 720s you'll consume a
   lot of orders.
3. Take **2-3 resource-monitor screenshots** across the 12 minutes (start,
   middle, end) — `evidence/resource-monitor/soak_start.png`,
   `soak_mid.png`, `soak_end.png` — so you can show whether memory/latency stayed
   flat or crept up over time.
4. After it finishes, read the Aggregate Report / `.jtl` and write down the
   concrete numbers the assignment wants: **max stable RPS** (throughput while
   error rate stayed low) and **memory ceiling** (peak `node.exe` working set from
   your screenshots, cross-checked against §0 step 1's starting free-memory
   figure). These numbers go in `main_report.md` and `README.md`.

## 7. GUI vs. headless (Spike / View Results Tree)

Apache JMeter's own documentation warns against using View Results Tree to
*generate* load in GUI mode — it holds full response data in memory live and can
freeze/OOM the GUI, especially at Spike's 150 threads (see Entry 09/10). Run all
four official scenarios **headless (`-n`)** as shown above — this is also just
correct performance-testing practice, not a workaround. If you want to visually
show View Results Tree's content for the demo video, do a **small, separate**
GUI-mode pass afterward (e.g., `jmeter` with no `-n`, a handful of requests) purely
to show the listener UI — that clip is illustrative, not the source of your
official Spike numbers/evidence.

## 8. After all four runs

Tell me you're done (or partially done) and paste/describe what you observed —
I'll help read the `.jtl`/HTML reports, write up the endurance-threshold numbers,
and move on to Task 2 (AI analysis of the logs) using your real data.
