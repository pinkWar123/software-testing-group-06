# Task 2 — AI Analysis (first pass, raw)

This is the **first-pass AI read** of the three real `.jtl` logs
(`results/{load,stress,spike}/*.jtl` — 1,115 / 6,465 / 2,210 samples
respectively, produced by your live official runs). Computed with
`analysis/compute_stats.js` directly against the raw CSVs (not estimated). This
pass is deliberately taken at face value here; `misinterpretation_hunt.md` is
the critical second pass that re-checks it.

## Headline numbers

| Scenario | n | Overall avg (ms) | p95 (ms) | Error rate (`success=false`) | Throughput |
|---|---|---|---|---|---|
| Load | 1,115 | 12.1 | 35 | 0.00% | 3.77 req/s |
| Stress | 6,465 | 1,432.6 | 2,478 | 0.00% | 35.95 req/s |
| Spike | 2,210 | 1,789.4 | 2,592 | 0.00% | 24.70 req/s |

## Reading

- **Load looks healthy across the board.** Sub-40ms p95 on every sampler, 0%
  errors. No concerns at 10 concurrent admins.
- **Stress shows a dramatic latency jump.** Average response time goes from
  ~12ms (Load) to ~1,433ms (Stress) — a ~118x increase — as concurrency goes
  from 10 to 80 threads. `GET /api/admin/orders` and
  `PUT /api/admin/orders/:id/status` degrade almost identically (avg 1,432.8ms
  vs. 1,454.0ms), which reads as the backend broadly struggling to keep up with
  80 concurrent users — classic stress-test saturation behavior.
- **Spike confirms the same ceiling.** Overall avg 1,789ms, p95 2,592ms, in the
  same range as Stress — consistent with 150 threads pushing the same backend
  even harder than Stress's 80.
- **Error rate is 0.00% everywhere**, which at first glance suggests the
  backend never actually fails under load, just slows down — a "graceful
  degradation" story rather than a "breaking point" story.

## Suggested performance thresholds (proposed)

- p95 response time budget: **≤ 200ms** for the admin order-management
  workflow (generous for an internal admin tool, well above Load's observed
  35ms).
- Error rate budget: **< 1%**.
- Based on the above, **Stress and Spike both breach the p95 budget by
  roughly 12x**, suggesting the current backend, as deployed on this hardware,
  comfortably handles Load-level concurrency (10 threads) but is well past a
  healthy operating point at Stress/Spike-level concurrency (80-150 threads).

## Proposed optimizations (for human judgment — see `optimization_judgment.md`)

1. **Add a database index** on the `orders` table to speed up the admin orders
   query.
2. **Introduce a connection pool** for the SQLite layer so concurrent requests
   aren't serialized on a single connection.
3. **Enable SQLite WAL (Write-Ahead Logging) mode** to improve concurrent
   read/write throughput.
4. **Add response caching** for `GET /api/admin/orders` so repeated reads
   don't hit the database every time.
