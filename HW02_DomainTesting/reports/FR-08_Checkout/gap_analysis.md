# FR-08 Gap Analysis

## Adversarial Review

The current FR-08 coverage correctly includes:
- authenticated checkout requirements,
- empty-cart rejection,
- tampered numeric `total_amount`,
- missing `shipping_address` UI coverage,
- cart clearing after checkout.

However, the current test set misses several domain-level adversarial cases that are directly implied by FR-08's requirement that the backend must compute and enforce checkout state independently of client input.

### Missing domain adversarial cases

1. Negative or non-numeric `total_amount`
   - Cause: the current tests focus on valid numeric tampering and do not cover malformed client payloads.
   - Why it matters: FR-08 requires the backend to ignore client-supplied totals and recompute from cart contents. If the backend accepts `-1000`, `"abc"`, `null`, or a missing field, that is a domain failure.

2. Checkout after a product is deleted from the catalog
   - Cause: the existing coverage assumes cart items remain valid after addition.
   - Why it matters: checkout must validate current cart item existence and business state, not merely trust the cart snapshot.

3. Two near-simultaneous checkouts by the same user (double-submit)
   - Cause: current tests are sequential and do not exercise concurrency or retry race conditions.
   - Why it matters: observed backend behavior already shows cart-clearing/order-creation issues; this gap can reveal duplicate orders or inconsistent cart state.

4. `shipping_address` containing unusual characters
   - Cause: the spec does not define format constraints, so this input was treated as GUI/security overlap instead of a domain-level persistence check.
   - Why it matters: backend checkout must accept valid address text and preserve it correctly. HTML/script rendering issues are GUI/security scope and should not count as FR-08 domain failures, but unusual unicode/punctuation should still be tested for checkout correctness.

## Missing Test Cases

| TC | Preconditions | Input / Action | Expected Domain Outcome | Status |
|---|---|---|---|---|
| TC-FR08-GAP-01 | User logged in; cart contains 1 valid item | `POST /api/checkout` with invalid `total_amount` values such as `-1000`, `"abc"`, `null`, or omitted field | Backend recomputes total from the cart and rejects malformed/negative client total; no order created | Not executed |
| TC-FR08-GAP-02 | User logged in; cart contains 1 item, then the item is removed from the product catalog | Delete the product from the catalog after adding it to cart; submit checkout | Backend validates current cart contents against catalog state, rejects checkout if item is deleted/unavailable | Not executed |
| TC-FR08-GAP-03 | User logged in; cart contains 1 item | Submit checkout twice in rapid succession using the same JWT and same cart state | Backend processes only one checkout, avoids duplicate orders, and leaves the cart state consistent | Not executed |
| TC-FR08-GAP-04 | User logged in; cart contains 1 item | `POST /api/checkout` with `shipping_address` containing unusual allowed characters, e.g. `123 Nguyễn Văn A, P.5, Q.10 / Apt #12B – 🚚` | Backend accepts the text address, preserves it correctly, and does not fail due to unusual unicode/punctuation | Not executed |

## Summary

These gaps are all directly aligned with FR-08's requirement that checkout be computed and enforced by the backend, independent of client input and stale cart state. They should be added to FR-08 coverage before concluding that checkout behavior is fully validated.
