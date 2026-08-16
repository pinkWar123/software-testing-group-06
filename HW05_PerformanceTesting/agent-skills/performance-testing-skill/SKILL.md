# Performance Testing + Log Analysis Skill

Purpose: reusable guided workflow for AI-assisted JMeter performance-test design
(Load/Stress/Spike/Soak), with mandatory human review, smoke-test verification
before any officially-recorded run, and disciplined `.jtl` log analysis with a
misinterpretation hunt. Built from and validated against the HW05 Performance
Testing assignment on the EShop SUT; reusable on a different endpoint group or a
different SUT with the same shape of problem.

## Principles (explicit)

- **One shared end-to-end workflow across all scenarios.** Load/Stress/Spike (and
  Soak) test the *same* multi-step workflow at different concurrency profiles —
  never a different workflow per scenario. Pick a workflow that naturally covers
  an auth-heavy step, a read-heavy step, and a transactional step.
- **Read the SUT's source before designing anything.** Don't assume textbook
  behavior (e.g., "3-strikes lockout," "always 200 on success"). Grep the actual
  auth/validation/state-machine logic first; document real thresholds/timings as
  binding ground rules before writing a single sampler.
- **AI-DRAFT → SMOKE-TEST → HUMAN-REVIEW → FIX, every scenario, no exceptions.**
  A draft is not "done" until it's been run for real (even at 1 thread/a few
  seconds) and critically re-read against JMeter's actual runtime semantics —
  not just "does the XML load," but "does the success/failure flag mean what I
  think it means." Log each of these as a separate, dated prompt/response entry.
- **JMeter's sampler-level success flag is not the same as an assertion
  passing.** Any HTTP response code ≥ 400 is marked a failed sample *before*
  assertions run; a `ResponseAssertion` can only turn a pass into a fail, never
  the reverse. Whenever an expected/valid outcome is a non-2xx code (a
  deliberately-rejected request, a business-rule 400, a lockout 403), use a
  `JSR223PostProcessor` that explicitly sets
  `prev.setSuccessful(prev.getResponseCode() == "<expected>")` — not a plain
  assertion. Apply this check to *every* new sampler that expects a non-2xx
  code, even ones added after you've "already learned the lesson" once in the
  same session — the fix doesn't generalize automatically; each new sampler
  needs its own scrutiny.
- **CSV-drive everything; never invent a fake mistake, but do document real
  ones.** If review finds nothing wrong, say so honestly rather than manufacture
  a defect — but do keep testing at successively higher scale (smoke → full
  run), since some bugs (like the assertion issue above) only show up once you
  revisit an already-transitioned record, which a 1-iteration smoke test won't
  naturally hit.
- **No fabricated evidence, ever.** `.jtl` logs, HTML reports, resource-monitor
  screenshots, and video must come from a run actually executed and watched by
  the human operator. The assistant may run non-evidentiary smoke tests to
  validate a plan, but never the official recorded run, and never invents
  numbers.
- **Seed data deliberately, and know when the SUT resets it.** Check whether
  starting the SUT wipes/reseeds its own database (common in demo apps) — if so,
  the seeding order is always: start SUT → seed test data → run test, every time,
  and document it as a rule, not a one-off gotcha.

## Skill steps (invokable)

1. **Ground the design in the real SUT.** Read the relevant source (auth logic,
   state machines, rate limits) and the API spec. Write down anything that
   contradicts a "reasonable default" assumption (e.g., lockout thresholds,
   response-code conventions) as a binding rule for every later step.
2. **Pick one shared workflow** covering auth-heavy + read-heavy + transactional
   endpoint groups. Confirm it doesn't duplicate a teammate's pick if this is a
   group assignment.
3. **Design parameters for one scenario at a time** (threads, ramp-up,
   think-time, duration) with a one-line justification each. Post the design for
   human sign-off *before* generating the `.jmx` — flag any decision with a real
   operational cost (e.g., "this will lock a shared account for 3 minutes") for
   explicit approval, not silent assumption.
4. **Generate the `.jmx` + CSVs.** Parameterize thread count/ramp-up/duration via
   `${__P(name,default)}` so the same file can be smoke-tested at tiny scale and
   run officially at full scale without editing XML.
5. **Smoke-test immediately** (1 thread, short duration) against the real,
   locally-running SUT. Confirm structural correctness (samplers fire, tokens
   correlate, CSVs resolve) — not full-scale correctness.
6. **Human-review pass.** Re-read the plan specifically for: assertion validity
   against JMeter's real success semantics (see Principles), realistic
   think-time/ramp-up, weak/missing assertions, and any endpoint-specific
   behavior (lockouts, rate limits) the draft might have ignored. Fix and
   re-smoke-test. Commit draft and fix as two separate commits so the diff is
   real, reviewable evidence — unless review genuinely finds nothing, in which
   case say so and commit once.
7. **Repeat 3-6 for each remaining scenario**, reusing the same workflow/CSVs.
8. **Hand off a live-execution runbook**, not silent execution. The assistant
   should never be the one pressing "go" on the officially-graded run — write
   exact commands, seeding steps, and screenshot/recording checkpoints for the
   human to execute and capture.
9. **Analyze the resulting `.jtl` logs in two passes.** First pass: a genuine,
   undirected AI read of the metrics (thresholds, p95/p99, error rate,
   throughput). Second pass: a deliberately skeptical re-read against the raw
   data looking for real misreadings (mean vs. percentile confusion, treating an
   expected non-2xx as an error, wrong units, cherry-picked windows) — cite the
   exact raw value being misread each time.
10. **Judge every AI-proposed optimization** (index, connection pool, caching,
    WAL mode, etc.) against the actual stack in use — feasible or hallucinated,
    with a one-line technical reason either way, not a blanket accept/reject.
11. **Propose a continuous-testing model** only after the manual results exist:
    a cheap gate for "should this even run," a smoke-vs-full split, a rolling
    (not static) baseline, and an explicit false-alarm mitigation.

## Usage notes

- The skill cannot capture screenshots, record video, or press "start" on a
  graded run — the human operator does all live execution and evidence capture.
  Batch and clearly checklist these requests (see `EXECUTION_RUNBOOK.md` for a
  worked example) rather than asking for one at a time mid-flow.
- Log every prompt/response pair as you go, in a single running Markdown file
  with a per-entry human "audit/correction" field — don't reconstruct the log
  from memory at the end.
- Always commit after a concrete, describable unit of work (one scenario's
  draft, one scenario's fix, one analysis pass) — never batch unrelated steps
  into one commit.

## Example invocation

"Run the performance-testing skill for the FR-07 shopping-cart workflow, JMeter,
against this repo's backend." The skill would: read `server.js`'s cart/checkout
handlers for any non-obvious behavior first, propose one shared
login→cart→checkout workflow, design and sign off Load parameters, build and
smoke-test the `.jmx`, review it against real JMeter success semantics, repeat
for Stress/Spike, hand off a runbook, then (once real `.jtl`s exist) run the
two-pass log analysis and optimization judgment.
