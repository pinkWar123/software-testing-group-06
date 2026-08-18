# Task 2 — Judging the AI's Optimization Recommendations

Each of the 4 optimizations the AI proposed in `ai_analysis_raw.md`, judged
against the actual stack: Express 5 + `sqlite3` (node-sqlite3), a single
shared `Database` connection opened once in `backend/database.js`, no ORM, no
pooling library, default (non-WAL) journal mode. Plus one the AI should have
proposed but didn't.

## 1. "Add a database index" — **Hallucinated** (for this bottleneck)

The slow query is `GET /api/admin/orders`:
`SELECT orders.*, users.name FROM orders LEFT JOIN users ON orders.user_id = users.id ORDER BY orders.id DESC`
([backend/server.js:510-523](../../backend/server.js#L510-L523)). The join
key (`users.id`) is the `users` table's `PRIMARY KEY`, already indexed; the
`ORDER BY orders.id DESC` sorts by the `orders` table's own `PRIMARY KEY`,
already indexed and cheap in SQLite. There's no `WHERE` clause filtering on
an unindexed column. Adding an index here would not measurably change the
query plan — the measured cost (`misinterpretation_hunt.md` #2) comes from
returning and serializing *every* row with no `LIMIT`, not from a missing
index. "Add an index" is generic database-performance advice that doesn't
engage with what this specific query actually does.

## 2. "Introduce a connection pool" — **Hallucinated**

This imports a mental model from client-server databases (MySQL/Postgres),
where pooling amortizes real per-connection costs (TCP handshake,
authentication). SQLite is an embedded, in-process, single-file database —
`backend/database.js` already opens one `sqlite3.Database` handle and reuses
it for the life of the process, which *is* the correct pattern here, not an
anti-pattern to fix. Critically, SQLite allows only **one writer at a time**
regardless of how many connection handles exist; opening more handles to the
same file doesn't parallelize writes and can add contention overhead of its
own. The AI's suggestion isn't nonsensical in general database terms, but
it's architecturally inapplicable to this stack as stated.

## 3. "Enable SQLite WAL mode" — **Feasible**

Confirmed via `backend/database.js`: no `PRAGMA journal_mode` is ever set, so
the database runs in SQLite's default rollback-journal mode, where writers
can block readers. `PRAGMA journal_mode = WAL` is a real, well-documented,
low-risk, one-line change (`db.run("PRAGMA journal_mode = WAL")` right after
opening the connection) that lets readers proceed concurrently with a writer
instead of blocking. Given the workload here is read-heavy
(`GET /api/admin/orders`) with interleaved writes
(`PUT /api/admin/orders/:id/status`), this is a legitimate, well-targeted
recommendation — genuinely worth doing, independent of the pagination fix
below.

## 4. "Add response caching for GET /api/admin/orders" — **Feasible, but not well-targeted**

Technically implementable (in-memory cache, ETag, etc.), but this endpoint's
data changes on every status update, so a cache needs an invalidation
strategy on every `PUT` — real complexity for an admin tool where showing
stale order state to staff is actively undesirable. The measured problem
(`misinterpretation_hunt.md` #2: ~342KB→1.7MB unbounded response payload) is
solved more directly and more simply by fix #5 below. Caching isn't wrong,
just a more complex answer to a problem that has a simpler fix already
available.

## 5. Pagination / `LIMIT` on `GET /api/admin/orders` — **Feasible, and conspicuously missing from the AI's own list**

Not proposed by the AI at all, despite being the single most directly
data-supported fix: the AI's own analysis had access to the `bytes` column
showing responses growing from ~342KB (Load) to ~1.7MB (Stress) as more
orders were seeded — the exact mechanism identified in
`misinterpretation_hunt.md` #2 as the likely dominant cause of the latency
blow-up under Stress/Spike (and, via Node's single-threaded event loop, a
plausible contributor to `PUT`'s latency too, despite `PUT` carrying a tiny,
constant ~335-byte payload of its own). Adding `LIMIT`/`OFFSET` (or
cursor-based pagination) to this query is a standard, low-effort, directly
evidenced fix — and its absence from the AI's proposal list, in favor of
generic textbook suggestions (index, pool, cache) that don't engage with the
specific numbers in front of it, is itself the most useful finding in this
whole judgment exercise: **the AI defaulted to boilerplate "database
performance 101" advice instead of reasoning from the data it had just
analyzed.**

## Summary table

| Optimization | Verdict | One-line reason |
|---|---|---|
| Database index | Hallucinated | Query already keyed on indexed primary keys; real cost is unbounded row count, not lookup cost |
| Connection pool | Hallucinated | SQLite is embedded/single-writer; the client-server pooling model doesn't apply |
| SQLite WAL mode | Feasible | Real, unset in this codebase, directly improves read/write concurrency |
| Response caching | Feasible, not well-targeted | Works, but adds invalidation complexity to solve what pagination solves directly |
| **Pagination/`LIMIT`** (human-added) | **Feasible — highest priority** | Directly matches the measured cause: unbounded, unpaginated response payload |
