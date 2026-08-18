# Task 2 — Misinterpretation Hunt (human review of the AI's analysis)

Re-checking `ai_analysis_raw.md` against the actual raw `.jtl` data (via
`analysis/compute_stats.js`, re-run per-claim below so every number here is
directly verifiable from `results/{load,stress,spike}/*.jtl`). Five real
misinterpretations found — none invented for the exercise; each one changes
what you'd actually conclude about the system.

---

### 1. "Error rate 0.00% everywhere" hides that ~85-98% of PUT calls were business rejections, not clean successes

**AI claimed:** 0.00% error rate across all three scenarios, framed as "the
backend never actually fails under load."

**Raw data:** `PUT /api/admin/orders/:id/status` response codes —
- Load: `{"200":58,"400":491}` → 87.8% of PUT calls got `400`.
- Stress: `{"200":381,"400":2798}` → 88.0% got `400`.
- Spike (Burst phase only): 920/937 = **98.2%** got `400`.

**The error:** `success=false` is 0.00% *by design* — the JSR223 PostProcessor
added during Load's human review (Entry 06) deliberately reclassifies `400
Invalid state transition` as successful, because it's an expected business
outcome once the seeded order pool is consumed. That fix is correct and
working exactly as intended. But the AI's summary conflated "0% marked-failed"
with "nothing interesting happening here" — when in fact the overwhelming
majority of PUT requests in every scenario are hitting already-transitioned
orders, not performing a fresh state change. That's a real signal about test
design (how large a pool was seeded relative to request volume), and it means
any latency/throughput claim about the PUT sampler is describing mostly
400-path behavior, not the 200-path — worth stating explicitly rather than
folding into a blanket "0% errors."

---

### 2. "GET and PUT degrade almost identically → broad concurrency saturation" ignores a real confound: unbounded, unpaginated response payloads

**AI claimed:** Stress's GET (avg 1,432.8ms) and PUT (avg 1,454.0ms) degrade
"almost identically," read as evidence of general backend saturation under 80
concurrent users.

**Raw data — average response size (`bytes` column):**
| Scenario | GET avg bytes | PUT avg bytes |
|---|---|---|
| Load | 342,796 | 336 |
| Stress | 1,716,940 | 335 |

**The error:** GET's payload is ~5x larger in Stress than in Load (because
Stress was seeded with roughly 5x more orders, per `EXECUTION_RUNBOOK.md`'s
suggested seed counts) — `GET /api/admin/orders` has no pagination
([backend/server.js:510-523](../../backend/server.js#L510-L523):
`SELECT orders.*, users.name ... ORDER BY orders.id DESC` with no `LIMIT`), so
every request serializes and returns the *entire* orders table. PUT's payload,
by contrast, is tiny and nearly constant across both scenarios (335-336
bytes) — it carries no order data. Yet PUT's latency degrades by roughly the
same *factor* as GET's (1454ms vs. Load's 5.1ms — a ~285x jump). Since PUT
isn't serializing anything large itself, its slowdown can't come from its own
payload — the much more plausible explanation is that Node's single-threaded
event loop is spending large amounts of time synchronously JSON-serializing
GET's multi-megabyte responses, which blocks *all* other in-flight requests
including PUT. The AI's "broad concurrency saturation" framing isn't wrong
that the system is struggling, but it attributes the cause purely to *thread
count*, when a large share of the effect is plausibly attributable to
*unbounded response size* — a confound introduced by how much data we seeded,
not purely by how many virtual users we ran. This matters because it points
to a specific, fixable cause (see `optimization_judgment.md` #1) rather than
a vague "the server can't handle 80 users."

---

### 3. Spike's "overall avg 1,789ms" blends three very different phases and misses the strongest finding: near-instant recovery

**AI claimed:** "Spike confirms the same ceiling" as Stress, citing an overall
average of 1,789.4ms across all 2,210 Spike samples.

**Raw data, segmented by Thread Group (Baseline/Burst/Recovery), computed from
the `threadName` field:**
| Phase | n | Avg elapsed (ms) | p95 (ms) |
|---|---|---|---|
| Baseline (before) | 58 | 21.2 | 51 |
| Burst (150 threads) | 2,091 | 1,890.0 | 2,594 |
| Recovery (after) | 61 | 20.5 | 56 |

**The error:** the single "overall average" the AI quoted is dominated by the
Burst phase simply because it contains 94.6% of all samples (2,091 of 2,210) —
Baseline and Recovery together are only 119 samples. Reporting one blended
number obscures the actual shape of a spike test, which is the entire point of
running Baseline→Burst→Recovery as separate phases. Worse, the AI's analysis
never mentions the Recovery figure at all — and Recovery (avg 20.5ms, p95
56ms) is nearly identical to Baseline (avg 21.2ms, p95 51ms), meaning **the
system fully recovers within seconds of the burst ending**. That's arguably
the single most important, most reassuring finding in this whole dataset, and
a blended "overall avg" analysis misses it entirely by construction.

---

### 4. The implied thread-count-to-latency relationship isn't linear, and the AI's phrasing suggests it might be

**AI claimed:** framed Stress (80 threads, avg 1,432.6ms) and Spike (150
threads, avg 1,789.4ms — really Burst's 1,890.0ms) as points on the same
"comfortably fine → well past healthy" continuum, implicitly scaling with
thread count.

**Raw data:** 80→150 threads is a 1.875x increase in concurrency; Stress's
1,432.6ms → Burst's 1,890.0ms is only a **1.32x** increase in average latency
— clearly sublinear. If the bottleneck scaled with thread count the way the
AI's narrative implies, 150 threads should look substantially worse than 1.32x
Stress's numbers, not modestly worse.

**The error:** treating "more threads = proportionally worse" as a safe
extrapolation. The sublinear relationship is actually consistent with the
payload-size bottleneck in #2: once Node's event loop is already saturated
serializing large GET responses at 80 concurrent threads, adding another 70
threads has a diminishing marginal effect, because the bottleneck isn't
"one thread per connection," it's a shared, single-threaded serialization
cost. This is a meaningfully different engineering conclusion (fix the
payload size; thread count past ~80 isn't the dominant lever) than what a
naive linear read would suggest.

---

### 5. Load's low PUT success rate (58/549 ≈ 10.6%) is a CSV data-sharing artifact, not a sign the endpoint "often rejects" updates

**Raw data:** Load ran 10 threads; only 58 of 549 PUT calls (10.6%) got a
fresh `200`. 549 / 58 ≈ 9.5 — close to the thread count itself.

**The error (one the raw first pass didn't make explicitly, but is an easy
trap when reading this number in isolation):** it's tempting to read a ~90%
non-fresh-transition rate as evidence of a stingy or flaky endpoint. The real
cause is the test's own CSV design: `order_ids.csv` is read with
`shareMode.thread` (Entry 04/05), meaning each of the 10 threads has an
*independent* read cursor — but all 10 start at row 1 at roughly the same
time (after the 20s ramp-up window), and all 10 share the same ~2s Gaussian
think-time distribution, so they advance through the file in near lock-step.
The result: at any given row, several threads race for the same `order_id`,
and only the first arrival gets a genuine `pending→confirmed` transition (a
fresh `200`) — the rest immediately see it's no longer `pending` and get
`400`. The ~1-in-10 success ratio lining up almost exactly with the 10-thread
count supports this explanation over "the endpoint is unreliable." This is a
property of how the test shares data across threads, not a defect in
`PUT /api/admin/orders/:id/status` itself.
