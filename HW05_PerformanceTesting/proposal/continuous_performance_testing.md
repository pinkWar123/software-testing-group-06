# Task 3 — Continuous Performance Testing Proposal

## Grounding

This proposal is built for the *actual* stack tested in this assignment — Express 5
+ `sqlite3` (single file, single process, `http://localhost:3000`), no external
services, JMeter as the load-generation tool, GitHub as the host. (The repo also
contains an untracked `.github/workflows/performance-test.yml` that references
MySQL, Redis, k6, Locust, and a `/health` endpoint — none of which exist in this
SUT. It looks like unwired boilerplate rather than a working pipeline, so this
proposal doesn't build on it; it's designed fresh against the real backend.)

## Goals

1. Every commit gets a cheap, fast signal on whether it changed anything
   performance-relevant.
2. Full Load/Stress/Spike/Soak runs are expensive and slow — reserve them for
   when they're actually warranted, not every push.
3. A p95 regression should be caught and reported automatically, without
   drowning the team in false alarms from normal CI noise.

## Flow

```mermaid
flowchart TD
    A[Commit pushed / PR opened] --> B{Changed paths touch\nbackend/** or jmeter/**?}
    B -- No --> C[Skip perf run\nPost "no perf-relevant changes" status]
    B -- Yes --> D{Is this a PR/push\nor the nightly schedule?}

    D -- PR/push --> E[Smoke perf check\n~60-90s reduced-thread Load pass\n1 endpoint group workflow]
    D -- Nightly / manual --> F[Full suite\nLoad + Stress + Spike + Soak\nsame .jmx plans as this HW]

    E --> G[Extract p95, error rate,\nthroughput from .jtl]
    F --> G

    G --> H{p95 > baseline p95 x 1.2\nOR error rate > 1%?}
    H -- No --> I[Update rolling baseline\n(main branch only)\nPost green status]
    H -- Yes --> J{Did it also regress\non a same-day re-run?}
    J -- No, looks like noise --> K[Post yellow warning comment\nwith numbers, do not fail build]
    J -- Yes, reproduced --> L[Fail the check\nPost red PR comment with\np95/baseline/error-rate table\nUpload .jtl + HTML report as artifact]
```

## Decision logic in detail

- **Path filter (cheap, first gate):** only run anything if the diff touches
  `backend/**`, `jmeter/**` (the test plans themselves), or the DB schema.
  Docs/frontend-only changes skip straight to green — this alone eliminates most
  unnecessary runs on a repo where perf-relevant changes are a minority of commits.
- **Smoke vs. full suite:** every PR/push gets a short, reduced-scale run of the
  same login→GET→PUT workflow validated in this homework (e.g., 10 threads/60s —
  a scaled-down Load), not the full Stress/Spike/Soak battery. Full suite runs
  nightly on a schedule, or on-demand via `workflow_dispatch` before a release.
  This mirrors why HW05 itself separates a 5-minute Load from a 12-minute Soak:
  different questions need different amounts of time to answer.
- **Baseline:** a rolling median p95 from the last N successful main-branch runs,
  stored as a build artifact (or a small JSON file committed by a bot on merge to
  main) — not a single magic number picked once and never revisited, since normal
  hardware/CI-runner variance would make a static baseline noisy within weeks.
- **Regression confirmation before failing the build:** a single run exceeding the
  threshold posts a warning, not a failure — shared CI runners are noisy (this
  homework's own Stress/Spike runs already show real variance from resource
  contention on a single laptop; a shared GitHub-hosted runner is worse). Require
  the regression to reproduce on a same-day re-run before it blocks anything.
  This is the single biggest lever against false alarms, at the cost of one extra
  run's worth of compute and a delayed signal.

## Trade-offs

| Dimension | Cheap/frequent (smoke, every push) | Expensive/rare (full suite, nightly) |
|---|---|---|
| **Cost** | Low — minutes per run, cheap to run on every PR | High — Stress+Spike+Soak together run ~20 min; daily is manageable, per-PR is not |
| **Signal speed** | Fast feedback to the author, same PR | Regressions surface up to 24h later, harder to attribute to a specific commit |
| **False-alarm risk** | Higher — short runs and noisy shared runners inflate variance; mitigated by the "confirm before failing" rule | Lower — longer runs average out noise, but a regression sits undetected longer if only caught nightly |
| **Coverage** | Only the smoke workflow depth; won't catch a regression that only appears at Stress/Spike concurrency | Full battery, catches concurrency-only regressions (e.g., the read-then-write race condition documented in `AGENTS.md`'s Known SUT characteristics) |

**Bottom line:** the smoke/full split exists specifically to buy fast per-PR
feedback without paying full-suite cost on every commit, while accepting that
concurrency-specific regressions (like the order-status race condition this
homework's design already flags as a risk) may only be caught by the nightly
full run, not the PR-time smoke check — a deliberate coverage-vs-cost trade-off,
not an oversight.
