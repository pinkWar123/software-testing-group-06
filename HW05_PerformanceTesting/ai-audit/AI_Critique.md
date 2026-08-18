# AI Critique (Task 1.10)

The clearest place the AI got something wrong was a mistake it repeated after
already fixing it once. While reviewing the Load plan, it correctly found that
JMeter marks any HTTP response code ≥400 as a failed sample before assertions
run, so a plain Response Assertion checking "code equals 400" can never rescue
an already-failed sample — it fixed this with a JSR223 PostProcessor. Minutes
later, building the Stress plan's lockout-validation samplers (which
deliberately expect 401/403, not 2xx), it used the exact same broken
Response-Assertion pattern again, and every lockout sample showed failed until
a second review caught it. The AI hadn't "learned" the lesson in any lasting
sense — fixing one instance didn't generalize to new code it wrote afterward
in the same session, even minutes later. That's a real limitation, not a
one-off slip: each new element needs the same scrutiny applied fresh, and a
human reviewer can't assume a corrected pattern will stick.

The AI's optimization suggestions during Task 2 were similarly revealing, in a
subtler way — not wrong exactly, but incomplete. Given the real `.jtl` data,
it proposed textbook fixes (a database index, a connection pool, caching) but
never proposed pagination, despite the response-size column in its own
analyzed data showing the actual mechanism (unbounded ~1.7MB JSON payloads) it
had just described as the likely bottleneck. It reached for generic
database-performance vocabulary instead of following its own evidence to the
most directly indicated fix.

The principle I take from both: AI output is only as reliable as the specific
check just run, not a standing property of the model going forward — every
claim, including its own prior claims, needs re-verification against the raw
data, every time.
