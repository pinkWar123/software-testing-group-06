# FR-15 — Product Management (CRUD, Admin)

- **Student ID:** 23127362
- **Feature:** FR-15 — Admin Product management: Create / Read / Update / Delete
- **Platform:** Web Admin `localhost:5174`
- **Technique:** Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
- **Domain source:** Specification in repo `ttbhanh/eshop-sut`, derived from the specification, not from source code.

**Source tags:** `[SPEC]` = constraint stated in the specification · `[ASSUMED]` = inferred, not stated in the spec · `[UI]` = boundary imposed by the UI / browser number type · `[OBS]` = conclusion reached by observing the running application.

## Specification excerpt

> FR-15: Admin can Add / View / Edit / Delete products. Input constraints — Product name: required, maximum 255 characters. Price: required, positive number (> 0). Category: required, must be chosen from the available list. When editing a product, only that product changes; all other products stay unchanged.

Consequences from the spec: name is required with an upper length bound of 255 (lower bound of 1 comes from "required", i.e. non-empty); price must be a number strictly greater than 0, with **no maximum defined** (no logical upper boundary); category is required but is selected from a fixed list; the distinctive property of Edit and Delete is **isolation** — other products must remain unchanged.

---

# Part A — Domain Testing (Equivalence Partitioning)

## Step 1 — Input / Output inventory

### Inputs

| # | Input | Type | Valid constraint | Source |
| --- | --- | --- | --- | --- |
| I1 | Product name | Text | Non-empty, length 1–255 | `[SPEC]` |
| I2 | Price | Number | `> 0`; no maximum defined | `[SPEC]` |
| I3 | Category | Selection | Chosen from the available list | `[SPEC]` |
| I4 | "Save product" button | Action | One click saves and shows a response | `[SPEC]` (response) / `[ASSUMED]` (click count) |
| I5 | "Delete" button | Action | Removes only the target product | `[SPEC]` |
| I6 | "Edit" button | Action | Changes only the target product | `[SPEC]` |
| I7 | Description / Image (if present in the form) | Text / URL | No constraint in FR-15 → optional | `[SPEC]` (absence of constraint) |

### Outputs

| # | Output | Expected | Source |
| --- | --- | --- | --- |
| O1 | Success / error toast | Appears after Save / Delete | `[SPEC]` |
| O2 | Product row in the admin list | Appears (Create) / updates (Edit) / disappears (Delete) | `[SPEC]` |
| O3 | Other products in the list | Unchanged after Edit / Delete | `[SPEC]` (isolation) |
| O4 | Price display format | `₫` with thousands separators | `[SPEC]` (FR-21) |
| O5 | Validation error message | Shown, positioned above the submit button | `[SPEC]` (FR-22) |
| O6 | Required-field marker `*` | Present on required fields | `[SPEC]` (FR-22) |

### Preconditions

- At least two products exist, so Edit / Delete isolation (O3) can be verified against a second product.
- Add-product form reachable by an authenticated admin account.

## Step 2 — Equivalence Classes

Name is a range on string length (required, ≤ 255): one valid class plus invalid classes split by reason (empty vs over-length). Price is a range with a strict lower bound (`> 0`): one valid class plus invalid classes split by reason (`≤ 0`, empty, non-numeric); a very large price is tagged `[UI]` because the spec sets no maximum — it is an overflow probe, not a spec-invalid class. Category is required-from-list; its invalid class (no/empty category) is **not reachable through the UI** — see note below.

### Input I1 — Product name

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-N1 | valid | Non-empty, 1–255 chars | Saved successfully | `[SPEC]` |
| EC-N2 | invalid | Empty | Rejected | `[SPEC]` |
| EC-N3 | invalid | Length > 255 | Rejected | `[SPEC]` |

### Input I2 — Price

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-P1 | valid | Number `> 0` | Saved successfully | `[SPEC]` |
| EC-P2 | invalid | `≤ 0` (includes `0` and negatives) | Rejected | `[SPEC]` |
| EC-P3 | invalid | Empty | Rejected | `[SPEC]` |
| EC-P4 | invalid | Non-numeric (e.g. `abc`) | Rejected | `[SPEC]` |
| EC-P5 | probe | Extremely large value | No maximum in spec; observe behaviour | `[UI]` |

### Input I3 — Category

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-C1 | valid | Selected from the available list | Saved successfully | `[SPEC]` |
| EC-C2 | invalid | No / empty category | **Not reachable via UI** — the form always has a default value and offers no empty option | `[OBS]` |

> **Category note `[OBS]`:** the invalid class EC-C2 cannot be exercised through the interface (a default is always selected, there is no blank option), so no valid rejection test can be run for it at the UI level. Backend-level enforcement is out of scope for this black-box UI test.

### Buttons (I4–I6)

| EC | Type | Situation | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-B1 | valid | "Save product", single click | Saved + response | `[SPEC]` |
| EC-B2 | probe | "Save product", rapid multiple clicks | Spec requires no debounce; observe how many products are created | `[ASSUMED]` |
| EC-B3 | valid | "Delete" on a product | That product removed; others unchanged | `[SPEC]` |
| EC-B4 | valid | "Edit" a product | Only that product changes; others unchanged | `[SPEC]` |

## Step 3 — Domain test cases

For valid classes, one test uses a typical non-boundary representative (name of a few chars, price `300000`) so that boundary values are reserved for Part B. For invalid classes, each test contains exactly one invalid factor while keeping every other factor valid, so a rejection cannot be masked. Read, Edit and Delete each get an explicit case; Edit and Delete additionally verify that a **second product stays unchanged**.

| TC | Operation | Name | Price | Button | Covers | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DT1 | Create | `Product A` | `300000` | Save ×1 | EC-N1, EC-P1, EC-C1, EC-B1 | Product added, response shown | `[SPEC]` | Product added, response shown | **Pass** |
| DT2 | Read | — | — | — | View | Created product shows correct name / price / category as a row in the list | `[SPEC]` | Created product shows correct name / price / category in the list | **Pass** |
| DT3 | Create | (empty) | `300000` | Save ×1 | EC-N2 | Rejected | `[SPEC]` | Empty name rejected | **Pass** |
| DT4 | Create | 256-char name | `300000` | Save ×1 | EC-N3 | Rejected | `[SPEC]` | 256-char name accepted; product added *(DT4.png)* | **Fail** |
| DT5 | Create | `Product A` | `-100` | Save ×1 | EC-P2 | Rejected | `[SPEC]` | Price `-100` accepted; product added *(DT5.png)* | **Fail** |
| DT6 | Create | `Product A` | `abc` | Save ×1 | EC-P4 | Rejected | `[SPEC]` | Field blocks non-numeric characters (only digits and `.` can be typed); `abc` cannot be entered → invalid input effectively rejected | **Pass** |
| DT7 | Create | `Product A` | (empty) | Save ×1 | EC-P3 | Rejected | `[SPEC]` | Empty price accepted; product added *(DT7.png)* | **Fail** |
| DT8 | Create | `Product A` | `99999999999999999999999` | Save ×1 | EC-P5 | Observe (no spec maximum) | `[UI]` | Very large price accepted; price displayed as `1e+23 ₫` (scientific notation, not a formatted price) *(DT8.png)* | **Fail** |
| DT9 | Create | `Product A` | `300000` | Save rapid ×N | EC-B2 | Observe how many products are created | `[ASSUMED]` | Rapid clicks create only one product | **Pass** |
| DT10 | Update | edit to `Product A2` | edit to `350000` | Save ×1 | EC-B4 | Only the edited product changes; a second product stays unchanged | `[SPEC]` | Price change not applied; **all** products get renamed instead of only the edited one (isolation violated) | **Fail** |
| DT11 | Update | (empty) | `300000` | Save ×1 | EC-N2 on edit | Rejected | `[SPEC]` | Empty name on edit rejected | **Pass** |
| DT12 | Update | 256-char name | `300000` | Save ×1 | EC-N3 on edit | Rejected | `[SPEC]` | 256-char name accepted on edit; price unchanged; **all** products renamed *(DT12.png)* | **Fail** |
| DT13 | Update | `Product A` | `-100` | Save ×1 | EC-P2 on edit | Rejected | `[SPEC]` | Price `-100` not applied; **all** products renamed *(DT13.png)* | **Fail** |
| DT14 | Delete | — | — | Delete | EC-B3 | Target product removed; a second product remains | `[SPEC]` | Target product removed; second product remains | **Pass** |

---

# Part B — Boundary Value Analysis

## Step 4 — Boundary analysis and boundary test cases

Two ordered fields qualify for BVA: name **length** and **price**. Name length has a lower boundary from "required" (between 0 and 1 character) and an upper boundary at 255. Price has a single lower boundary at the constant `0`, because the rule is `price > 0`; `0` is the on-boundary point and must be **rejected** — this is the point that catches a `>` vs `>=` off-by-one error, so it is kept even though it is a rejection. Price has no spec maximum, so its large values are UI/overflow probes tagged `[UI]`. Each boundary test contains a single value under test.

### Name length — lower boundary (required) — `[SPEC]`

| BV | Length | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV1 | 0 (empty) | LB − 1 | Rejected | `[SPEC]` |
| BV2 | 1 | LB | Accepted | `[SPEC]` |
| BV3 | 2 | LB + 1 | Accepted | `[SPEC]` |

### Name length — upper boundary (255) — `[SPEC]`

| BV | Length | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV4 | 254 | UB − 1 | Accepted | `[SPEC]` |
| BV5 | 255 | UB | Accepted | `[SPEC]` |
| BV6 | 256 | UB + 1 | Rejected | `[SPEC]` |

### Price — lower boundary (constant = 0, rule `> 0`) — `[SPEC]`

| BV | Value | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV7 | `-1` (negative) | below | Rejected | `[SPEC]` |
| BV8 | `0` | on (LB) | Rejected — catches `>` vs `>=` | `[SPEC]` |
| BV9 | smallest positive accepted (`1`; also try `0.1`) | above | Accepted | `[SPEC]` / `[ASSUMED]` (decimals) |

### Price — upper boundary — UI / overflow only — `[UI]`

| BV | Value | Meaning | Expected | Source |
| --- | --- | --- | --- | --- |
| BV10 | `99999999999999999999999` | Very large number | No spec maximum; observe math / display | `[UI]` |

### Adversarial / malformed inputs — `[ASSUMED]`

- **Name:** all-whitespace `"   "` (does "required" trim to empty?) · leading / trailing spaces · multibyte characters near the limit — Vietnamese diacritics (`ậ`) or emoji, to check whether the limit is **255 characters or 255 bytes**.
- **Price:** `1e3` · `1,000` · `+5` · `2.0` · `0.1` (decimal) · leading / trailing spaces · `0x10` · very long digit string.

### Boundary test cases

| TC | Field | Value | Position | Covers BV | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BT1 | Name | 0 chars (empty) | LB − 1 | BV1 | Rejected | `[SPEC]` | Empty name rejected | **Pass** |
| BT2 | Name | 1 char | LB | BV2 | Accepted, response shown | `[SPEC]` | 1-char name accepted | **Pass** |
| BT3 | Name | 2 chars | LB + 1 | BV3 | Accepted, response shown | `[SPEC]` | 2-char name accepted | **Pass** |
| BT4 | Name | 254 chars | UB − 1 | BV4 | Accepted, response shown | `[SPEC]` | 254-char name accepted | **Pass** |
| BT5 | Name | 255 chars | UB | BV5 | Accepted, response shown | `[SPEC]` | 255-char name accepted | **Pass** |
| BT6 | Name | 256 chars | UB + 1 | BV6 | Rejected | `[SPEC]` | 256-char name accepted; product added *(BT6.png)* | **Fail** |
| BT7 | Price | `-1` | below | BV7 | Rejected | `[SPEC]` | Price `-1` accepted; product added *(BT7.png)* | **Fail** |
| BT8 | Price | `0` | on | BV8 | Rejected | `[SPEC]` | Price `0` accepted; product added *(BT8.png)* | **Fail** |
| BT9 | Price | `1` (and `0.1`) | above | BV9 | Accepted, response shown | `[SPEC]` | `1` and `0.1` accepted | **Pass** |
| BT10 | Price | `99999999999999999999999` | far above (UI) | BV10 | Observe (no spec maximum) | `[UI]` | Very large price accepted; displayed as `1e+23 ₫` (scientific notation) — same behaviour as DT8 *(DT8.png)* | **Fail** |

---

## Step 5 — AI gap analysis

- **Large-value expectation corrected.** The initial draft expected a very large price to be "rejected". The specification defines no maximum price, so a large value is not spec-invalid; the expectation was changed to an observation tagged `[UI]`. This is the same trap as the invented stock limit in FR-06 — expectations must come from the spec, not from what seems reasonable.
- **Category invalid class is unreachable, not "always valid".** The draft dismissed category as "always valid". Running the app showed the invalid class (no category) cannot be reached through the UI because a default is always selected and no empty option exists. This is recorded as an observation (`[OBS]`) about test reachability rather than a claim that the input has no constraint.
- **Read operation was missing.** CRUD has four operations; the draft covered Create, Update and Delete but not Read. A Read case (DT2) was added so all four are exercised.
- **Isolation property under-tested.** The distinctive FR-15 rule — only the target product changes on Edit / Delete — was not explicitly verified. DT10 and DT14 now check that a second product stays unchanged.
- **Boundary point `0` retained for price.** `0` is the on-boundary value for the rule `> 0`; keeping it is what detects a `>=` off-by-one defect, so it stays as a rejection case (BV8) rather than being dropped.
- **Edit defect far worse than the isolation check anticipated.** The design treated Edit isolation as a single pass/fail expectation (DT10). Execution revealed a systemic defect: editing any product renames **every** product and silently drops the price change. The real severity only surfaced by running the tests, not from the spec-derived design.

## Step 6 — Bug report

> To be filled after running the tests and confirming each defect. Open a GitHub Issue per confirmed bug on the team repo and paste the link.

| Bug ID | Title | Severity | Steps to reproduce | Expected | Actual | Screenshot | Issue link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-01 | Price field accepts invalid values (`0`, negative, empty) | Major | Add or edit a product; set Price to `0` (also `-1`, `-100`, or cleared); click Save | Input rejected / not saved | Product is saved in every case | DT5.png, DT7.png, BT7.png, BT8.png | #41 |
| BUG-02 | Product name longer than 255 characters is accepted | Major | Add or edit a product; set the name to a 256-character string; click Save | Rejected (max 255) | Product is saved with the over-length name | DT4.png, BT6.png | #42 |
| BUG-03 | Editing one product renames ALL products and does not apply the price change (isolation broken) | Critical | Have at least two products; edit one product's name and price; click Save | Only the edited product changes; others stay unchanged | Every product is renamed to the new name; the price change is not applied | DT12.png, DT13.png | #43 |
| BUG-04 | Very large price accepted and shown in scientific notation (`1e+23 ₫`), no maximum | Minor | Add a product; set Price to `99999999999999999999999`; click Save; view the list | A reasonable value; price formatted with `₫` and separators | Value accepted; displayed as `1e+23 ₫` instead of a formatted number | DT8.png | #44 |

---

## Test summary

- Domain test cases designed: **14** (DT1–DT14)
- Boundary test cases designed: **10** (BT1–BT10)
- Total designed: **24**
- Executed: **24** · Passed: **13** · Failed: **11** · Not run: **0**
- Bugs found: **4** (BUG-01 – BUG-04)

*Failed:* DT4, DT5, DT7, DT8, DT10, DT12, DT13, BT6, BT7, BT8, BT10. All other cases passed.