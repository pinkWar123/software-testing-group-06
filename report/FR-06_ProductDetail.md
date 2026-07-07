# FR-06 — Product Detail (Quantity field)

- **Student ID:** 23127362
- **Feature:** FR-06 — Product Detail, Quantity input + "Add to cart" button
- **Platform:** Web `localhost:5173`
- **Technique:** Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
- **Domain source:** Specification in repo `ttbhanh/eshop-sut`, derived from the specification, not from source code.

**Source tags:** `[SPEC]` = constraint stated in the specification · `[ASSUMED]` = inferred, not stated in the spec · `[UI]` = boundary imposed by the UI / browser number type.

## Specification excerpt

> FR-06: the Quantity input accepts positive integers only, minimum 1. The Add to cart button, after clicking, shows a visual response (toast notification or badge update).

Consequences from the spec: valid domain of Quantity is integer `>= 1`; no maximum value is defined (no logical upper boundary); no stock/inventory concept; the required output is a visual response (toast or badge).

---

# Part A — Domain Testing (Equivalence Partitioning)

## Step 1 — Input / Output inventory

### Inputs

| # | Input | Type | Valid constraint | Source |
| --- | --- | --- | --- | --- |
| I1 | Quantity | Number | Integer, `>= 1` | `[SPEC]` |
| I2 | "Add to cart" button | Action | Click once → add to cart + show response | `[SPEC]` (response) / `[ASSUMED]` (click count) |
| I3 | Variant / size selector, if present | Selection | Confirm existence in the application | `[ASSUMED]` |

### Outputs

| # | Output | Expected | Source |
| --- | --- | --- | --- |
| O1 | Visual response (toast / badge) | Appears after click | `[SPEC]` |
| O2 | Cart quantity badge | Increases by the entered amount | `[SPEC]` |
| O3 | Input field state after click | Defined and consistent | `[ASSUMED]` |
| O4 | Cart total | A valid number, not `NaN` | `[ASSUMED]` |
| O5 | Error message on invalid input | Reports or blocks the input | `[SPEC]` |

### Preconditions

- Behaviour of add-to-cart when logged out vs logged in.
- Presence of a variant/size selector on the detail page (promotes I3 to a real input).
- Repeated add of the same product accumulates quantity (belongs to FR-07).

## Step 2 — Equivalence Classes

The only spec-constrained input is Quantity, whose rule is a range with a lower bound (`integer >= 1`). Applying the guideline for a range — one valid class plus one invalid class per distinct reason for rejection — the invalid side is split by reason: below the minimum, wrong type (decimal), empty, and non-numeric. Applying the guideline "split a class if its elements may not be handled identically", negatives (EC6) are separated from `0` (EC2), since sign handling in code often differs from a plain `0`. EC7 (very large) is tagged `[UI]` because the spec defines no maximum; it is not a spec class but an overflow probe used in Part B.

### Input I1 — Quantity

| EC | Type | Domain | Expected | Source |
| --- | --- | --- | --- | --- |
| EC1 | valid | Integer `>= 1` | Added to cart, response shown | `[SPEC]` |
| EC2 | invalid | `0` | Rejected / not added | `[SPEC]` |
| EC3 | invalid | Decimal (e.g. `1.5`) | Rejected (integers only) | `[SPEC]` |
| EC4 | invalid | Empty | Rejected / not added | `[SPEC]` |
| EC5 | invalid | Non-numeric string (e.g. `abc`) | Rejected | `[SPEC]` |
| EC6 | invalid | Negative (e.g. `-1`) | Rejected | `[SPEC]` |
| EC7 | invalid | Extremely large value (overflow) | No maximum in spec; observe behaviour | `[UI]` |

### Input I2 — Add to cart button

| EC | Type | Situation | Expected | Source |
| --- | --- | --- | --- | --- |
| EC-B1 | valid | Click once | Added to cart + response | `[SPEC]` |
| EC-B2 | invalid | Rapid multiple clicks while processing | Spec does not require debounce; observe number added | `[ASSUMED]` |

## Step 3 — Domain test cases (selected from the equivalence classes)

For valid classes, one test uses a single typical representative (`Quantity = 5`), chosen deliberately as a non-boundary value so that boundary values are reserved for Part B. For invalid classes, each test covers one and only one invalid class while keeping every other factor valid, so that a rejection cannot be masked by a second invalid input.

| TC | Quantity | Button | Covers EC | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DT1 | `5` | click once | EC1, EC-B1 | Add 5 items, response shown | `[SPEC]` | 5 items added, response shown | **Pass** |
| DT2 | `0` | click once | EC2 | Rejected / not added | `[SPEC]` | `0` accepted; item added to cart instead of being rejected *(DT2-5 and 7.png)* | **Fail** |
| DT3 | `-1` | click once | EC6 | Rejected | `[SPEC]` | `-1` accepted; item added instead of being rejected *(DT2-5 and 7.png)* | **Fail** |
| DT4 | `1.5` | click once | EC3 | Rejected | `[SPEC]` | `1.5` silently truncated to `1`; 1 item added and response shown, no error *(DT2-5-and-7.png)* | **Fail** |
| DT5 | (empty) | click once | EC4 | Rejected; cart total not `NaN` | `[SPEC]` | Empty value accepted; item added instead of being rejected *(DT2-5-and-7.png)* | **Fail** |
| DT6 | `abc` | click once | EC5 | Rejected; cart total not `NaN` | `[SPEC]` | Field blocks non-numeric characters at keystroke level — `abc` cannot be entered, so the invalid input is effectively rejected | **Pass** |
| DT7 | `9999999999` | click once | EC7 | Observe (overflow, see Part B) | `[UI]` | `9999999999` accepted; math and display correct at this magnitude, but no reasonable upper cap is enforced *(DT2-5-and-7.png)* | **Fail** *(no reasonable upper limit; overflow shown in BT5)* |
| DT8 | `5` | rapid multiple clicks | EC-B2 | Observe number added | `[ASSUMED]` | Button ignores rapid repeat clicks, but after adding it changes to an "Added" button; clicking that "Added" button adds the same product to the cart **again** *(DT8.png)* | **Fail** |

---

# Part B — Boundary Value Analysis

## Step 4 — Boundary analysis and boundary test cases

Quantity is an ordered field, so it qualifies for BVA. The spec defines only a lower boundary, min = 1, giving the three points `0, 1, 2`. The spec defines no maximum, so there is no logical upper boundary; the large values below are boundaries imposed by the UI / browser `number` type and are tagged `[UI]`. Unusual numeric formats are then probed to see where parsing or validation leaks. Each boundary test contains a single value under test.

### Lower boundary of I1 (min = 1) — `[SPEC]`

| BV | Value | Position | Expected | Source |
| --- | --- | --- | --- | --- |
| BV1 | `0` | LB − 1 | Rejected | `[SPEC]` |
| BV2 | `1` | LB | Accepted | `[SPEC]` |
| BV3 | `2` | LB + 1 | Accepted | `[SPEC]` |

### Upper boundary — UI / overflow only — `[UI]`

| BV | Value | Meaning | Expected | Source |
| --- | --- | --- | --- | --- |
| BV4 | `9999999999` | Very large number | Computed / displayed correctly | `[UI]` |
| BV5 | `9007199254740991` | `Number.MAX_SAFE_INTEGER` | No overflow | `[UI]` |
| BV6 | `9007199254740992`+ | Beyond MAX_SAFE_INTEGER | Observe incorrect math | `[UI]` |
| BV7 | Digit string longer than field maxlength | Character overflow | Observe truncation point | `[UI]` |

### Adversarial / malformed numeric formats — `[ASSUMED]`

`"  "` (whitespace) · `" 5 "` · `+5` · `1e3` · `1,000` · `1.000` · `2.0` · `1.5.2` · `0x10` · special characters / emoji.

### Boundary test cases

| TC | Quantity | Position | Covers BV | Expected | Source | Actual | Pass/Fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BT1 | `0` | LB − 1 | BV1 | Rejected | `[SPEC]` | `0` accepted; item added instead of being rejected *(BT1.png)* | **Fail** |
| BT2 | `1` | LB | BV2 | Accepted, response shown | `[SPEC]` | Accepted, item added, response shown | **Pass** |
| BT3 | `2` | LB + 1 | BV3 | Accepted, response shown | `[SPEC]` | Accepted, item added, response shown | **Pass** |
| BT4 | `9999999999` | far above (UI) | BV4 | Correct math / display | `[UI]` | Value accepted; cart math / display correct at this magnitude | **Pass** |
| BT5 | `9007199254740992` | beyond MAX_SAFE_INTEGER | BV6 | Observe overflow | `[UI]` | Beyond MAX_SAFE_INTEGER; math / display incorrect (floating-point overflow) *(BT5.png)* | **Fail** |
| BT6 | `+5` / `1e3` / `1,000` / `2.0` | malformed format | adversarial | Observe validation | `[ASSUMED]` | Quantity is silently auto-corrected to another value; no error shown *(BT6.png)* | **Fail** |

---

## Step 5 — AI gap analysis

- **Invented constraint (stock).** When assisting with this feature, the AI initially introduced a stock/inventory constraint on Quantity that does not exist in the specification, and treated it as an upper boundary. This was retracted after checking the specification, which defines no maximum. The domain must follow the spec rather than plausible-sounding constraints the AI adds on its own.
- **Wrong suspicion about the button defect.** A code-reading note had suspected the "Add to cart" button "misses the first click and needs two clicks". Running the app did **not** confirm this; the real defect is different — after a successful add the button turns into an "Added" button that re-adds the same product when clicked again (DT8). Code-reading suspicions can mislabel the actual defect; the true behaviour only surfaced by executing the black-box tests.
- **Input-level blocking not predicted.** The spec-derived design assumed non-numeric input would be entered and then rejected with a message. In practice the field blocks non-numeric characters at keystroke level (DT6), a behaviour a black-box, spec-only design could not predict — noted because it also affects how the DT6 verdict should be argued.

## Step 6 — Bug report

> Severities are proposed; confirm before opening GitHub Issues. Issue links to be filled after creating each issue on the team repo.

| Bug ID | Title | Severity | Steps to reproduce | Expected | Actual | Screenshot | Issue link |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-01 | Quantity field accepts invalid values (`0`, negative, empty) | Major | Open a product detail page; set Quantity to `0` (or `-1`, or clear it); click Add to cart | Input rejected / not added | Item is added to the cart | DT2-5-and-7.png, BT1.png | #32 |
| BUG-02 | Decimal quantity silently truncated to integer with no message | Minor | Set Quantity to `1.5`; click Add to cart | Rejected (integers only) | Silently truncated to `1` and added; response shown, no error | DT2-5-and-7.png | #33 |
| BUG-03 | No maximum quantity; very large values accepted and overflow beyond MAX_SAFE_INTEGER | Major | Set Quantity to `9999999999`, then to `9007199254740992`; click Add to cart | Reasonable handling; correct math | `9999999999` accepted; values beyond MAX_SAFE_INTEGER produce incorrect math / display | DT2-5-and-7.png, BT5.png | #34 |
| BUG-04 | Malformed numeric formats silently auto-corrected | Minor | Set Quantity to `+5` / `1e3` / `1,000` / `2.0`; click Add to cart | Rejected or clearly handled | Quantity is silently auto-corrected to another value, no error | BT6.png | #35 |
| BUG-05 | "Added" button re-adds the same product on repeat click (double-add) | Major | Set a valid Quantity; click Add to cart; when the button becomes "Added", click it again | Product added once; further clicks do not duplicate | The product is added to the cart again | DT8.png | #36 |

---

## Test summary

- Domain test cases designed: **8** (DT1–DT8)
- Boundary test cases designed: **6** (BT1–BT6)
- Total designed: **14**
- Executed: **14** · Passed: **5** · Failed: **9** · Not run: **0**
- Bugs found: **5** (BUG-01 – BUG-05)

*Passed:* DT1, DT6, BT2, BT3, BT4. *Failed:* DT2, DT3, DT4, DT5, DT7, DT8, BT1, BT5, BT6.