# FR-09 — Discount Coupon — Domain Testing & BVA

| Field | Value |
| --- | --- |
| Feature | FR-09 — Mã giảm giá |
| Pool / Platform | B / Web checkout (`localhost:5173`) |
| Spec source | EShop SRS §4, FR-09 |
| Tester | 23127362 |

## Spec summary — coupon applies only if ALL 5 conditions hold
- C1 code exists and `is_active = 1`
- C2 not expired (today < `expired_at`)
- C3 order total `>= min_order_amount`
- C4 user logged in (valid JWT)
- C5 usage per user `< max_uses_per_user`

Discount: `percent` -> total × value / 100; `fixed` -> value. `final = total - discount`.

### Sample coupons (from spec)
| Code | Type | Value | Min order | Expiry | Uses/user |
| --- | --- | --- | --- | --- | --- |
| SAVE10 | percent | 10% | 300,000 | 2099-12-31 | 1 |
| BIGBUY | fixed | 50,000 | 500,000 | 2099-12-31 | 1 |
| VIP100 | fixed | 100,000 | 300,000 | 2099-12-31 | 2 |
| EXPIRED | percent | 20% | 100,000 | 2020-01-01 | 1 |

---

## Step 1 — Input inventory
| # | Input | Type | Valid domain | Notes |
| --- | --- | --- | --- | --- |
| I1 | Coupon code | string | one of active codes | C1 |
| I2 | Order total | money | >= min_order_amount | C3 threshold |
| I3 | Auth state | boolean | logged in | C4 |
| I4 | Usage count | integer | < max_uses_per_user | C5 |
| I5 | Current date vs expiry | date | today < expired_at | C2 |

## Step 2 — Domain Testing (decision-table style, C1–C5)
<!-- Build a decision table: each condition True/False, one representative test per
     meaningful combination. Start from the "all pass" happy path, then flip one
     condition at a time to isolate each rejection reason. -->
| EC-ID | Scenario | C1 | C2 | C3 | C4 | C5 | Expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EC1 | all valid (SAVE10, total>=300k, logged in, 1st use) | T | T | T | T | T | discount applied |
| EC2 | code not exist | F | - | - | - | - | reject |
| EC3 | expired (EXPIRED) | T | F | T | T | T | reject |
<!-- continue: flip C3, C4, C5 individually -->

## Step 3 — Boundary Value Analysis (on the numeric/date thresholds)
| BV-ID | Boundary | Value tested | Side | Expected |
| --- | --- | --- | --- | --- |
| BV1 | min_order (SAVE10 = 300,000) | 299,999 | below | reject (C3) |
| BV2 | min_order | 300,000 | on (>=) | accept |
| BV3 | min_order | 300,001 | above | accept |
| BV4 | expiry date | day before / on / after `expired_at` | around | check C2 |
| BV5 | uses/user (SAVE10 = 1) | 0th, 1st, 2nd use | around | 2nd use reject (C5) |

## Step 4 — Test cases
| TC-ID | Technique | Title | Precondition | Test data / steps | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC01 | EP | Happy path SAVE10 | cart total 300,000, logged in | apply SAVE10 | -30,000 |  |  |

## Step 5 — AI gap analysis
- Missed:
- Why:

## Step 6 — Bugs found
| BUG-ID | Title | Severity | Steps | Expected | Actual | Issue link |
| --- | --- | --- | --- | --- | --- | --- |
