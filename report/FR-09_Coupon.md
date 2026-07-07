# FR-09 — Discount Coupon

- **Student ID:** 23127362
- **Feature:** FR-09 — Apply discount coupon at cart / checkout
- **Platform:** Web `localhost:5173`
- **Technique:** Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
- **Domain source:** Specification in repo `ttbhanh/eshop-sut`, derived from the specification, not from source code.

**Source tags:** `[SPEC]` = constraint stated in the specification · `[ASSUMED]` = inferred, not stated in the spec · `[UI]` = boundary imposed by the UI / browser number type.

## Specification excerpt

> FR-09: A coupon applies only when **all** 5 conditions hold — **C1** code exists and `is_active = 1`; **C2** not expired (`today < expired_at`); **C3** order total `>= min_order_amount`; **C4** user is logged in (valid JWT); **C5** the user's usage count `< max_uses_per_user`. Discount: `percent` -> `total * value / 100`; `fixed` -> `value`. Final total = `total - discount`.

Seeded sample coupons: `SAVE10` (percent 10%, min 300,000, uses/user 1) · `BIGBUY` (fixed 50,000, min 500,000, uses/user 1) · `VIP100` (fixed 100,000, min 300,000, uses/user 2) · `EXPIRED` (percent 20%, min 100,000, expiry 2020-01-01, uses/user 1).

---

# Part A — Domain Testing (Equivalence Partitioning)

## Step 1 — Input / Output inventory

### Inputs

| # | Input | Type | Valid constraint | Source |
| --- | --- | --- | --- | --- |
| I1 | Coupon code | String | Exists in DB & `is_active = 1` | `[SPEC]` (C1) |
| I2 | Login state | Auth | User has a valid JWT | `[SPEC]` (C4) |
| I3 | Order total | Number | `>= min_order_amount` | `[SPEC]` (C3) |
| I4 | User's usage history for the code | Number | Times used `< max_uses_per_user` | `[SPEC]` (C5) |
| I5 | Current date | Date | Before `expired_at` | `[SPEC]` (C2) |
| I6 | "Apply" button | Action | Click to submit the code for validation | `[ASSUMED]` |

### Outputs

| # | Output | Expected | Source |
| --- | --- | --- | --- |
| O1 | Error message | Clearly states the reason if any of the 5 conditions fails | `[SPEC]` |
| O2 | Discount amount (`discount_amount`) | Computed correctly per `percent` or `fixed` type | `[SPEC]` |
| O3 | Final total (`final_amount`) | `total - discount_amount` | `[SPEC]` |
| O4 | Bill / cart UI | Updates immediately after a successful apply | `[ASSUMED]` |

### Preconditions

- Sample coupons seeded into the database: `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`.
- Cart already contains products so there is a concrete order total.

## Step 2 — Equivalence Classes

Since the spec defines 5 mandatory conditions, the equivalence classes are split per condition (true/false) and per coupon type (percent/fixed) to also check the calculation formula.

### Business rules (valid / invalid conditions)

| EC | Type | Domain / Condition | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-C1 | valid | Code correct, in DB, active | Proceed to check C2–C5 | `[SPEC]` |
| EC-C1-Inv | invalid | Code wrong, empty, or `is_active = 0` | Error: code does not exist / invalid | `[SPEC]` |
| EC-C2 | valid | Current date `< expired_at` | Apply | `[SPEC]` |
| EC-C2-Inv | invalid | Current date `>= expired_at` (e.g. `EXPIRED`) | Error: coupon expired | `[SPEC]` |
| EC-C3 | valid | Total `>= min_order_amount` | Apply | `[SPEC]` |
| EC-C3-Inv | invalid | Total `< min_order_amount` | Error: order total below minimum | `[SPEC]` |
| EC-C4 | valid | User logged in | Apply | `[SPEC]` |
| EC-C4-Inv | invalid | User not logged in (guest) | Error / require login | `[SPEC]` |
| EC-C5 | valid | Times used `< max_uses_per_user` | Apply successfully | `[SPEC]` |
| EC-C5-Inv | invalid | Times used `>= max_uses_per_user` | Error: usage limit reached | `[SPEC]` |

### Calculation

| EC | Type | Condition | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-CAL-1 | valid | `percent` type | Discount = `total * value / 100` | `[SPEC]` |
| EC-CAL-2 | valid | `fixed` type | Discount = `value` | `[SPEC]` |

## Step 3 — Domain test cases (selected from equivalence classes)

For valid cases, the math is checked for both coupon types. For invalid cases, four conditions are kept valid and exactly one is made invalid, so the system's rejection can be attributed to that single condition (one invalid at a time).

| TC | Code | Logged in | Total | Usage | Covers EC | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DT1 | `SAVE10` | Yes | `400,000` | 0 | All valid, EC-CAL-1 | Applied. Discount `40,000` (10%). Final `360,000` | `[SPEC]` | Discount shown as `360,000` (i.e. 90% / the after-discount value) instead of `40,000`; total stays `400,000`, coupon not actually applied *(DT1.png)* | **Fail** |
| DT2 | `BIGBUY` | Yes | `600,000` | 0 | All valid, EC-CAL-2 | Applied. Discount `50,000` (fixed). Final `550,000` | `[SPEC]` | Applied correctly, discount `50,000`, final `550,000` | **Pass** |
| DT3 | `INVALID` | Yes | `500,000` | 0 | EC-C1-Inv | Error: code does not exist / invalid | `[SPEC]` | Error: invalid code | **Pass** |
| DT4 | (empty) | Yes | `500,000` | 0 | EC-C1-Inv | Apply button disabled or empty-input error | `[SPEC]` | No apply when empty | **Pass** |
| DT5 | `EXPIRED` | Yes | `200,000` | 0 | EC-C2-Inv | Error: coupon expired | `[SPEC]` | Error: coupon expired | **Pass** |
| DT6 | `SAVE10` | Yes | `200,000` | 0 | EC-C3-Inv | Error: order below 300,000 | `[SPEC]` | Error: order below 300,000 | **Pass** |
| DT7 | `SAVE10` | No | `400,000` | n/a | EC-C4-Inv | Error: login required to use a coupon | `[SPEC]` | Coupon **still applies** even when not logged in — C4 is not enforced *(DT7.png)* | **Fail** |
| DT8 | `SAVE10` | Yes | `400,000` | 1 | EC-C5-Inv | Error: usage limit reached (limit=1, already used 1 so not `< 1`) | `[SPEC]` | Error: usage limit reached | **Pass** |

---

# Part B — Boundary Value Analysis

## Step 4 — Boundary analysis and boundary test cases

The coupon **code** is an unordered string, so it has no boundary — it belongs to Domain Testing (C1). The boundaries in FR-09 come from the **ordered thresholds inside the conditions**: order total vs `min_order_amount` (C3), the **expiry date** (C2), and the **usage count** (C5). C1 and C4 are boolean and have no boundary. Each boundary test keeps every other condition valid so the threshold under test is the only variable — therefore, for the C5 and overflow tests, the **order total is set above the threshold (`400,000`)** so it cannot be confused with the C3 threshold defect.

### Boundary C3 — Order total vs `min_order_amount` (coupon `SAVE10`, min = 300,000) — `[SPEC]`

| BV | Total | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV1 | `299,999` | LB − 1 | Rejected (below minimum) | `[SPEC]` |
| BV2 | `300,000` | LB (=) | Applied — catches `>` vs `>=` | `[SPEC]` |
| BV3 | `300,001` | LB + 1 | Applied | `[SPEC]` |

### Boundary C2 — Expiry date (`today < expired_at`) — `[SPEC]`

To exercise this, use admin to create test coupons expiring yesterday / today / tomorrow; the clearly-past case uses `EXPIRED` (2020).

| BV | Coupon expiry vs today | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV-D1 | yesterday (or `EXPIRED`) | past | Rejected (expired) | `[SPEC]` |
| BV-D2 | today | on | Observe: `today < expired_at` implies expired when equal — confirm whether still usable "on the day" | `[ASSUMED]` |
| BV-D3 | tomorrow | future | Applied | `[SPEC]` |

### Boundary C5 — Usage count vs `max_uses_per_user` (coupon `VIP100`, max = 2) — `[SPEC]`

Spec states `times used < max`. With max = 2: used 0, 1 (valid) and 2 (invalid) — a classic off-by-one point if the code uses `<=` instead of `<`.

| BV | Times used | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV4 | `1` | UB − 1 | `1 < 2` (True) -> applied | `[SPEC]` |
| BV5 | `2` | UB | `2 < 2` (False) -> rejected (limit reached) | `[SPEC]` |

### Adversarial / edge cases — `[ASSUMED]` / `[UI]`

| BV | Situation | Meaning | Expected | Source |
| --- | --- | --- | --- | --- |
| BV6 | `discount_amount > total` | Fixed coupon larger than the cart | `final_amount` not negative (e.g. = 0); no money refunded to the customer | `[ASSUMED]` |
| BV7 | Very large cart (e.g. 10 billion) with a percent coupon | Overflow when computing percent | Correct math, no font/layout break | `[UI]` |

### Boundary test cases

| TC | Code | Total | Usage | Covers BV | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BT1 | `SAVE10` | `299,999` | 0 | BV1 | Rejected, "below minimum" error | `[SPEC]` | Rejected, below-minimum error | **Pass** |
| BT2 | `SAVE10` | `300,000` | 0 | BV2 | Applied. Discount `30,000`, final `270,000` | `[SPEC]` | **Not applied**, shows "below 300000" — off-by-one; should be accepted since `300000 >= 300000` *(BT2.png)* | **Fail** |
| BT3 | `SAVE10` | `300,001` | 0 | BV3 | Applied (threshold accepted correctly) | `[SPEC]` | Applied at `300,001` (threshold OK); the discount amount itself is wrong due to the percent bug — see BUG-01 | **Pass** |
| BT4 | `VIP100` | `400,000` | 1 | BV4 | Applied (1 < 2) | `[SPEC]` | Applied (1 < 2); total set above threshold so C5 is tested in isolation from C3 | **Pass** |
| BT5 | `VIP100` | `400,000` | 2 | BV5 | Rejected, limit reached (2 < 2 false) | `[SPEC]` | Rejected; total above threshold so the reason is "limit reached", not C3 | **Pass** |
| BT6 | fixed coupon | `50,000` | 0 | BV6 | `final_amount` not negative (= 0 or rejected) | `[ASSUMED]` | **Not run** — every sample fixed coupon has `min_order_amount` >= its discount value, so C3 blocks this before it can be reached. Testing it needs an "apply then reduce cart" flow (apply while total >= min, then remove items to drop the total) | **Not run** |
| BT7 | `SAVE10` | `9,999,999,999` | 0 | BV7 | Observe large-number handling: correct math, no crash / layout break | `[UI]` | Large number: displays without crash or layout break; the percent discount value is still affected by BUG-01 | **Pass** |

---

## Step 5 — AI gap analysis

- **The "C4 is unreachable" assumption was WRONG.** C4 (not logged in) was initially suspected to be unreachable through the UI because checkout requires login. Running the app showed the coupon **still applies** while logged out (DT7) — not only reachable, but a bug: C4 is not enforced. Lesson: do not conclude a class is "untestable" before actually running it.
- **The on-boundary BVA point proved its value.** Keeping `300,000` (exactly on the threshold, `>=`) caught a real off-by-one bug (BT2): the system rejects at the exact threshold and only applies after adding at least 1 more — the code uses `>` instead of `>=`. Dropping the on-boundary point would have missed this bug entirely.
- **Conditions were entangled when testing C5.** The first run set the total exactly on the threshold (`300,000`) while testing C5 for `VIP100`, so the result was contaminated by the C3 off-by-one bug (unclear whether the rejection was "limit reached" or "below minimum"). Fixed by setting the total above the threshold (`400,000`) to isolate C5. Lesson: when testing one condition, the other conditions should not merely be "valid" but should be kept **away from their own boundaries**.
- **BT6 confirmed a design concern.** The `discount_amount > total` case is unreachable with the sample data (every coupon's threshold is >= its discount value); reaching it needs an "apply then reduce cart" flow.

## Step 6 — Bug report

| Bug ID | Title | Severity | Steps to reproduce | Expected | Actual | Screenshot | Issue link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-01 | Percent coupon miscalculated and not applied to the total | Major | Log in; cart total `400,000`; apply `SAVE10` (10%) | Discount `40,000`, final `360,000` | Discount shown as `360,000` (~90% / the after-discount value); total stays `400,000`, coupon not applied | DT1.png |#49|
| BUG-02 | Coupon applies while not logged in (C4 bypassed) | Major | Not logged in; cart total `400,000`; apply `SAVE10` | Require login / reject | Coupon applies successfully | DT7.png |#50 |
| BUG-03 | Order-total threshold uses `>` instead of `>=` (off-by-one) | Major | Apply any coupon with total = exactly `min_order_amount` (e.g. `SAVE10` at `300,000`) | Applied successfully | Rejected as "below minimum"; must add at least 1 more to apply | BT2.png |#51 |

---

## Test summary

- Domain test cases designed: **8** (DT1–DT8)
- Boundary test cases designed: **7** (BT1–BT7)
- Total designed: **15**
- Executed: **14** · Passed: **11** · Failed: **3** · Not run: **1**
- Bugs found: **3** (BUG-01 – BUG-03)

*Failed:* DT1, DT7, BT2. *Not run:* BT6. *Passed:* all other cases.