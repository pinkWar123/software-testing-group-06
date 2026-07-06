# FR-06 — Product Detail (Quantity Input) — Domain Testing & BVA

| Field | Value |
| --- | --- |
| Feature | FR-06 — Xem chi tiết sản phẩm |
| Pool / Platform | A / Web (`localhost:5173`) |
| Spec source | EShop SRS §3, FR-06 |
| Tester | 23127362 |

## Spec summary
- Displays: image, name, price, description, category.
- **Quantity** input: positive integer, minimum 1.
- "Add to cart" button gives visual feedback (toast / badge).

---

## Step 1 — Input inventory

| # | Input | Type | Valid domain | Notes / dependencies |
| --- | --- | --- | --- | --- |
| I1 | Quantity | integer | >= 1 (positive integer) | may also be limited by stock — verify in app |
| I2 | Add-to-cart button | action | — | feedback expected |

## Step 2 — Domain Testing (Equivalence Partitioning)

| EC-ID | Input | Valid/Invalid | Class description | Representative |
| --- | --- | --- | --- | --- |
| EC1 | Quantity | Valid | positive integer within range | 1 |
| EC2 | Quantity | Invalid | zero / negative | 0 |
| EC3 | Quantity | Invalid | non-integer (decimal) | 1.5 |
| EC4 | Quantity | Invalid | non-numeric | "abc" |
| EC5 | Quantity | Invalid | empty | "" |
| EC6 | Quantity | Invalid | very large / overflow | 999999 |
<!-- add/adjust classes as you explore the real app -->

## Step 3 — Boundary Value Analysis

| BV-ID | Input | Boundary | Value | Side | Expected |
| --- | --- | --- | --- | --- | --- |
| BV1 | Quantity | lower (min=1) | 0 | below | reject |
| BV2 | Quantity | lower | 1 | on | accept |
| BV3 | Quantity | lower | 2 | above | accept |
<!-- add upper boundary rows if a max (e.g. stock) applies -->

## Step 4 — Test cases

| TC-ID | Technique | Title | Precondition | Test data / steps | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC01 | EP/BVA | Min valid quantity | on product page | set qty=1, add to cart | added, badge=1 |  |  |
| TC02 |  |  |  |  |  |  |  |
<!-- fill from EC + BV above; dedupe overlapping values -->

## Step 5 — AI gap analysis
- Test cases / bugs the AI missed:
- Why (prompt quality / AI limitation / feature complexity):

## Step 6 — Bugs found
| BUG-ID | Title | Severity | Steps | Expected | Actual | Issue link |
| --- | --- | --- | --- | --- | --- | --- |
