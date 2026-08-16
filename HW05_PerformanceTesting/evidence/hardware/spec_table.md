# Hardware Spec Table

Gathered directly from the test machine via `systeminfo` / `wmic` (2026-08-16,
`c:\Users\ACER\Downloads\eshop-sut`). Pair this with a `dxdiag` screenshot
(`evidence/hardware/dxdiag.png`, captured by the student — required by the
assignment's anti-cheat rule that the hostname match prior HW deployments).

| Field | Value |
|---|---|
| Hostname | `LAPTOP-HNGLK6L4` |
| System | Acer Aspire A515-58GM |
| OS | Windows 11 Home Single Language, 10.0.26200 (Build 26200) |
| CPU | 13th Gen Intel(R) Core(TM) i5-13420H — 8 cores / 12 logical processors |
| RAM (total) | 16,088 MB (~16 GB) |
| RAM (available at capture time) | 2,099 MB — **note:** background apps were already
  using most of the machine's memory when this was captured; re-check available
  memory right before each official run and close unnecessary apps, since the
  soak test's "memory ceiling" finding is only meaningful relative to what was
  actually free at the time. |
| Node.js | v22.19.0 |
| npm | 11.6.3 |
| JMeter | 5.6.3 (`D:\apache-jmeter-5.6.3`) |
| Backend | Express 5 + `sqlite3` 6, single process, `http://localhost:3000` |

**To do (student):** capture `dxdiag` screenshot and save as
`evidence/hardware/dxdiag.png`; re-run `systeminfo` right before the official
recorded sessions if you want an exact "available memory at test time" figure
instead of this snapshot.
