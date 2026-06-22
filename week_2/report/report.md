# HW02 — Domain Testing on EShop
## Main Report

**Student ID:** 22127345
**Date:** June 2026
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut

---

## Table of Contents

1. [Feature Selection](#1-feature-selection)
2. [Feature A — \[FR-XX: Name\]](#2-feature-a)
   - 2.1 Domain Testing
   - 2.2 Boundary Value Analysis
   - 2.3 AI Gap Analysis
   - 2.4 Bug Report
3. [Feature B — \[FR-XX: Name\]](#3-feature-b)
   - 3.1 Domain Testing
   - 3.2 Boundary Value Analysis
   - 3.3 AI Gap Analysis
   - 3.4 Bug Report
4. [Feature C — \[FR-XX: Name\]](#4-feature-c)
   - 4.1 Domain Testing
   - 4.2 Boundary Value Analysis
   - 4.3 AI Gap Analysis
   - 4.4 Bug Report
5. [Feature D — \[FR-XX: Name, Mobile\]](#5-feature-d)
   - 5.1 Domain Testing
   - 5.2 Boundary Value Analysis
   - 5.3 AI Gap Analysis
   - 5.4 Bug Report
6. [AI Critique](#6-ai-critique)
7. [Mandatory Disclosure](#7-mandatory-disclosure)
8. [Appendix A — Prompt Log](#8-appendix-a)

---

## 1. Feature Selection

| Pool | Feature ID | Feature Name | Reason for Selection |
|------|-----------|--------------|----------------------|
| A | FR-02 | Login and account lockout | Randomly selected; rich boundary conditions on lockout threshold and credential inputs |
| B | FR-07 | Shopping cart | Randomly selected; complex domain with quantity, price, and stock constraints |
| C | FR-17 | Coupon management (CRUD) | Randomly selected; multiple constrained fields (discount value, date range, usage limit) |
| D | Mobile | Mobile App — general feature | Randomly selected (Pool D) |

---

## 2. Feature A — FR-02: Login and Account Lockout

### 2.1 Domain Testing

#### Step-by-step Technique Application

**Step 1 — Understand the feature from source code**

Endpoint: `POST /api/login` (Body: `{ email, password }`)

Key logic discovered from `backend/server.js`:
1. Looks up user by `email` (exact string match in DB).
2. If user not found → 401 "Invalid email or password".
3. If `user.locked_until` is set AND is in the future → 403 locked error.
4. If `user.password === password` (plain-text comparison, no hashing) → login success, reset `login_attempts = 0`.
5. On wrong password: `newAttempts = user.login_attempts + 2` (**Bug found: increments by 2, not 1**).
6. If `newAttempts >= 3` → set `locked_until = now + 3 minutes (180,000 ms)`.

**Step 2 — Identify input variables**

| Variable | Type | Description |
|----------|------|-------------|
| `email` | string | Account identifier — looked up in DB |
| `password` | string | Credential — compared as plain text |
| `account_state` | derived | Combination of `login_attempts` and `locked_until` in DB |

**Step 3 — Define domains (equivalence classes) for each variable**

**Variable: `email`**
| Domain | Class | Representative Value |
|--------|-------|----------------------|
| D-E1 | Valid: registered, well-formed email | `test@eshop.com` |
| D-E2 | Invalid: unregistered but well-formed email | `nobody@eshop.com` |
| D-E3 | Invalid: malformed (no `@`) | `testeshop.com` |
| D-E4 | Invalid: empty string | `""` |
| D-E5 | Invalid: null / missing field | `null` |

**Variable: `password`**
| Domain | Class | Representative Value |
|--------|-------|----------------------|
| D-P1 | Valid: correct password for the account | `Test1234!` |
| D-P2 | Invalid: wrong password (non-empty string) | `WrongPass99` |
| D-P3 | Invalid: empty string | `""` |
| D-P4 | Invalid: null / missing field | `null` |

**Variable: `account_state`**
| Domain | Class | Condition |
|--------|-------|-----------|
| D-S1 | Clean (never failed) | `login_attempts = 0`, `locked_until = NULL` |
| D-S2 | One-failed (at-risk) | `login_attempts = 2`, `locked_until = NULL` ← after 1 wrong attempt due to +2 bug |
| D-S3 | Actively locked | `locked_until` set to a future timestamp |
| D-S4 | Lock expired | `locked_until` set to a past timestamp |

**Step 4 — Identify boundary points**

The key boundary is the lockout threshold: **`newAttempts >= 3`**

With the +2 increment bug:
- After attempt 1 (wrong): `newAttempts = 0 + 2 = 2` → **2 < 3 → NOT locked** (on point of "safe" side)
- After attempt 2 (wrong): `newAttempts = 2 + 2 = 4` → **4 >= 3 → LOCKED** (lockout triggered)

| Variable | Boundary | On Point | Off Point | In Point | Out Point |
|----------|----------|----------|-----------|----------|-----------|
| `newAttempts` vs lockout threshold (3) | `>= 3` triggers lock | `newAttempts = 3` (never reachable with +2 bug) | `newAttempts = 2` (just below — no lock) | `newAttempts = 0` (clean) | `newAttempts = 4` (locked) |
| `locked_until` vs `now` | lock active if `locked_until > now` | `locked_until ≈ now` | `locked_until` 1 ms before now (expired) | `locked_until = NULL` | `locked_until = now + 3 min` |

**Step 5 — Design test cases** (one variable varied at a time; others held at in-point)

---

#### Test Cases

| TC ID | Objective | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-A-01 | Valid login (clean account) | email: `test@eshop.com`, password: `Test1234!` | Account clean (`login_attempts=0`) | POST /api/login with valid credentials | 200 OK, JWT token returned | | |
| TC-A-02 | Unregistered email (D-E2) | email: `nobody@eshop.com`, password: `Test1234!` | N/A | POST /api/login | 401 "Invalid email or password" | | |
| TC-A-03 | Malformed email — no @ (D-E3) | email: `testeshop.com`, password: `Test1234!` | N/A | POST /api/login | 401 error or 400 bad request | | |
| TC-A-04 | Empty email (D-E4) | email: `""`, password: `Test1234!` | N/A | POST /api/login | 401 error | | |
| TC-A-05 | Missing email field (D-E5) | No email field, password: `Test1234!` | N/A | POST /api/login | 401 or 400 error | | |
| TC-A-06 | Wrong password — 1st attempt (D-P2, off point: newAttempts=2) | email: `test@eshop.com`, password: `WrongPass99` | `login_attempts=0` | POST /api/login | 401 error; account NOT locked (newAttempts=2 < 3) | | |
| TC-A-07 | Wrong password — 2nd attempt (on point: newAttempts=4, triggers lock) | email: `test@eshop.com`, password: `WrongPass99` | `login_attempts=2` (after TC-A-06) | POST /api/login | 401 error; account LOCKED for 3 minutes | | |
| TC-A-08 | Login while actively locked (D-S3) | email: `test@eshop.com`, password: `Test1234!` | Account locked (`locked_until` in future) | POST /api/login | 403 "Tài khoản đã bị khóa. Vui lòng thử lại sau." | | |
| TC-A-09 | Login after lock expires (D-S4) | email: `test@eshop.com`, password: `Test1234!` | `locked_until` set to past timestamp | POST /api/login | 200 OK, login success; lock ignored | | |
| TC-A-10 | Correct password after 1 failed attempt (D-S2) | email: `test@eshop.com`, password: `Test1234!` | `login_attempts=2` | POST /api/login | 200 OK, `login_attempts` reset to 0 | | |
| TC-A-11 | Empty password (D-P3) | email: `test@eshop.com`, password: `""` | Clean account | POST /api/login | 401 "Invalid email or password" | | |
| TC-A-12 | Missing password field (D-P4) | email: `test@eshop.com`, no password | Clean account | POST /api/login | 401 or 400 error | | |

### 2.2 Boundary Value Analysis

_[To be filled in with /bva skill]_

### 2.3 AI Gap Analysis

_[To be filled after test execution]_

### 2.4 Bug Report

_[To be filled after test execution]_

| Bug ID | Title | Severity | Steps to Reproduce | Expected | Actual | GitHub Issue |
|--------|-------|----------|--------------------|----------|--------|--------------|

---

## 3. Feature B — FR-07: Shopping Cart

### 3.1 Domain Testing

#### Step-by-step Technique Application

**Step 1 — Understand the feature from source code**

Endpoints:
- `GET /api/cart` — returns in-memory cart for current user
- `POST /api/cart` — pushes any body object directly into cart array (no server-side validation)
- `POST /api/checkout` — creates order with `total_amount` and `shipping_address`

Key observations from `backend/server.js` and `frontend-mobile/App.js`:
1. **Server-side cart has NO validation** — any `quantity`, `price`, even negative values are accepted.
2. Cart is **in-memory** (`userCarts` object) — resets on server restart.
3. The mobile app's `normalizeQuantity()` does client-side normalization: `parseInt(value) > 0 ? parsed : 1`.
4. Cart total: `cart.reduce((total, item) => total + item.price * item.quantity, 0)`.
5. `checkout` accepts any `total_amount` value — no server-side verification against cart contents.

**Step 2 — Identify input variables**

| Variable | Type | Source |
|----------|------|--------|
| `quantity` | integer (string in UI) | User input in cart |
| `price` | integer | Taken from product data |
| `total_amount` | integer | Passed at checkout |
| `shipping_address` | string | User input at checkout |

**Step 3 — Define domains for each variable**

**Variable: `quantity` (POST /api/cart body)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-Q1 | Valid: positive integer ≥ 1 | `1`, `5`, `100` |
| D-Q2 | Invalid: zero | `0` |
| D-Q3 | Invalid: negative integer | `-1`, `-100` |
| D-Q4 | Invalid: non-integer string | `"abc"`, `"one"` |
| D-Q5 | Invalid: float/decimal | `1.5`, `0.9` |
| D-Q6 | Invalid: empty / null | `""`, `null` |

**Variable: `total_amount` (POST /api/checkout)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-T1 | Valid: positive integer > 0 | `100000`, `500000` |
| D-T2 | Invalid: zero | `0` |
| D-T3 | Invalid: negative | `-100000` |
| D-T4 | Invalid: non-numeric | `"abc"` |
| D-T5 | Invalid: null / missing | `null` |

**Variable: `shipping_address` (POST /api/checkout)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-A1 | Valid: non-empty string | `"123 Le Loi, Q1, TP.HCM"` |
| D-A2 | Invalid: empty string | `""` |
| D-A3 | Invalid: null / missing | `null` |

**Step 4 — Identify boundary points**

| Variable | Boundary | On Point | Off Point | In Point | Out Point |
|----------|----------|----------|-----------|----------|-----------|
| `quantity` (mobile normalizeQuantity: `> 0`) | `parsed > 0` | `1` (just valid) | `0` (just invalid → normalized to 1) | `5` | `-1` |
| `total_amount` at checkout | `> 0` | `1` | `0` | `100000` | `-1` |

**Step 5 — Design test cases**

---

#### Test Cases

| TC ID | Objective | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-B-01 | Add item with valid quantity (D-Q1, in point) | `{id:1, name:"X", price:100000, quantity:5}` | Logged in | POST /api/cart | 200 "Added to cart"; cart has item with quantity=5 | | |
| TC-B-02 | Add item with quantity=1 (on point, min valid) | `{..., quantity:1}` | Logged in | POST /api/cart | 200; quantity=1 accepted | | |
| TC-B-03 | Add item with quantity=0 (off point, D-Q2) | `{..., quantity:0}` | Logged in | POST /api/cart | Should reject (400) or treat as invalid | | |
| TC-B-04 | Add item with negative quantity (D-Q3) | `{..., quantity:-1}` | Logged in | POST /api/cart | Should reject (400) | | |
| TC-B-05 | Add item with non-integer quantity string (D-Q4, mobile) | Quantity input = `"abc"` in mobile UI | Logged in, on product detail | Tap "Add to cart" | Mobile normalizes to 1; item added with quantity=1 | | |
| TC-B-06 | Add item with float quantity (D-Q5, mobile) | Quantity input = `"1.5"` | Logged in | Tap "Add to cart" | Mobile: `parseInt("1.5")=1`, item added with quantity=1 | | |
| TC-B-07 | Checkout with valid total_amount (D-T1) | `{total_amount:200000, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | 200, order created with `status=pending` | | |
| TC-B-08 | Checkout with total_amount=0 (off point, D-T2) | `{total_amount:0, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | Should reject; order with 0 total should be invalid | | |
| TC-B-09 | Checkout with negative total_amount (D-T3) | `{total_amount:-1, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | Should reject (400) | | |
| TC-B-10 | Checkout with empty shipping_address (D-A2) | `{total_amount:200000, shipping_address:""}` | Cart has items | POST /api/checkout | Should reject (400) — address required | | |
| TC-B-11 | Checkout with arbitrary total_amount (bypasses UI) | `{total_amount:1, shipping_address:"addr"}` | Cart has items worth 500,000 | POST /api/checkout directly (API) | Server accepts any value — no cart-total verification | | |
| TC-B-12 | Add same product twice (quantity accumulation) | Add product id=1 twice with qty=3 each | Cart empty | 2× POST /api/cart | Cart shows product id=1 with quantity=6 | | |

### 3.2 Boundary Value Analysis

_[To be filled]_

### 3.3 AI Gap Analysis

_[To be filled after test execution]_

### 3.4 Bug Report

| Bug ID | Title | Severity | Steps to Reproduce | Expected | Actual | GitHub Issue |
|--------|-------|----------|--------------------|----------|--------|--------------|

---

## 4. Feature C — FR-17: Coupon Management (CRUD)

### 4.1 Domain Testing

#### Step-by-step Technique Application

**Step 1 — Understand the feature from source code**

Endpoints:
- `POST /api/admin/coupons` — admin creates coupon (requires auth)
- `DELETE /api/admin/coupons/:id` — admin deletes coupon
- `POST /api/apply-coupon` — user applies coupon (public)
- `GET /api/coupons` — list all coupons (requires auth)

Coupon schema (`database.js`):
```
code TEXT UNIQUE, type TEXT DEFAULT 'percent',
discount_value INTEGER, min_order_amount INTEGER DEFAULT 0,
expired_at DATETIME, is_active INTEGER DEFAULT 1, max_uses_per_user INTEGER DEFAULT 1
```

Key apply-coupon logic (`server.js` lines 363–436):
1. Lookup coupon by `code` where `is_active = 1` — not found → error.
2. Check: `if (total_amount > coupon.min_order_amount)` — strict `>` (not `>=`).
3. Check expiry: `new Date(coupon.expired_at) >= new Date()` — past date → error.
4. Check usage: `usage_count >= coupon.max_uses_per_user` → error.
5. Calculate discount:
   - `percent` type: `Math.floor(total_amount * (1 - coupon.discount_value))` — **Bug: stores integer (e.g., 10), should be 0.10; produces negative result (1-10 = -9)!**
   - `fixed` type: `discount_amount = coupon.discount_value` → correct.

**Step 2 — Identify input variables**

For admin CREATE coupon:

| Variable | Type | Constraint |
|----------|------|-----------|
| `code` | TEXT UNIQUE | Must be unique |
| `type` | TEXT | Should be `'percent'` or `'fixed'` |
| `discount_value` | INTEGER | Positive number; % type buggy |
| `min_order_amount` | INTEGER | ≥ 0 |
| `expired_at` | DATETIME | Future date |
| `max_uses_per_user` | INTEGER | ≥ 1; defaults to 1 |

For apply-coupon:

| Variable | Domains |
|----------|---------|
| `code` | valid active code, invalid/inactive code |
| `total_amount` | > min_order_amount (valid), = min_order_amount (boundary!), < min_order_amount |
| expiry date | future (valid), past (invalid) |
| usage count | < max (valid), = max (boundary, invalid), > max |

**Step 3 — Define domains**

**Variable: `total_amount` vs `min_order_amount` (apply-coupon)**
| Domain | Class | Note |
|--------|-------|------|
| D-M1 | Valid: `total_amount > min_order_amount` | `total=300001`, `min=300000` |
| D-M2 | Boundary: `total_amount = min_order_amount` | `total=300000`, `min=300000` — rejected (strict `>`) |
| D-M3 | Invalid: `total_amount < min_order_amount` | `total=299999`, `min=300000` |

**Variable: expiry (`expired_at`)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-X1 | Valid: future date | `2099-12-31` |
| D-X2 | Boundary: today/same day | current date |
| D-X3 | Invalid: past date | `2020-01-01` |

**Variable: `usage_count` vs `max_uses_per_user`**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-U1 | Valid: `usage_count < max_uses_per_user` | count=0, max=1 |
| D-U2 | Boundary (on): `usage_count = max_uses_per_user` | count=1, max=1 → rejected |
| D-U3 | Over: `usage_count > max_uses_per_user` | count=2, max=1 |

**Variable: `code` (admin CREATE)**
| Domain | Class |
|--------|-------|
| D-C1 | Valid: unique code string | `"NEWCODE"` |
| D-C2 | Invalid: duplicate code | `"SAVE10"` (already exists) |
| D-C3 | Invalid: empty string | `""` |

**Variable: `type` (admin CREATE)**
| Domain | Class |
|--------|-------|
| D-T1 | Valid: `"percent"` |
| D-T2 | Valid: `"fixed"` |
| D-T3 | Invalid: unsupported type | `"cashback"`, `""` |

**Step 4 — Identify boundary points**

| Variable | Boundary condition | On point | Off point | In point | Out point |
|----------|-------------------|----------|-----------|----------|-----------|
| `total_amount` vs `min_order_amount=300000` | `total > min` | `300001` | `300000` (rejected) | `500000` | `299999` |
| `expired_at` vs now | `expiry >= now` | today's date | yesterday | `2099-12-31` | `2020-01-01` |
| `usage_count` vs `max_uses_per_user=1` | `count >= max` → block | count=1 | count=0 (still allowed) | count=0 | count=2 |

**Step 5 — Design test cases**

---

#### Test Cases

| TC ID | Objective | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-C-01 | Create coupon with unique code (D-C1) | `{code:"TEST50", type:"fixed", discount_value:50000, min_order_amount:200000, expired_at:"2099-12-31", max_uses_per_user:1}` | Admin logged in | POST /api/admin/coupons | 200 "Coupon created" | | |
| TC-C-02 | Create coupon with duplicate code (D-C2) | `{code:"SAVE10", ...}` | `SAVE10` already exists | POST /api/admin/coupons | 500 error (UNIQUE constraint violated) | | |
| TC-C-03 | Apply coupon with total > min_order (D-M1, in point) | `{code:"SAVE10", total_amount:300001, user_id:1}` | SAVE10 exists, min=300000 | POST /api/apply-coupon | 200, discount applied | | |
| TC-C-04 | Apply coupon with total = min_order (D-M2, off point) | `{code:"SAVE10", total_amount:300000, user_id:1}` | SAVE10 exists, min=300000 | POST /api/apply-coupon | Error: minimum order not met (strict `>`) | | |
| TC-C-05 | Apply coupon with total < min_order (D-M3, out point) | `{code:"SAVE10", total_amount:299999, user_id:1}` | SAVE10 exists, min=300000 | POST /api/apply-coupon | Error: minimum order not met | | |
| TC-C-06 | Apply expired coupon (D-X3) | `{code:"EXPIRED", total_amount:200000, user_id:1}` | EXPIRED coupon `expired_at=2020-01-01` | POST /api/apply-coupon | Error: coupon expired | | |
| TC-C-07 | Apply valid coupon first use (D-U1, in point) | `{code:"SAVE10", total_amount:500000, user_id:1}` | 0 prior uses, max=1 | POST /api/apply-coupon | 200, discount applied | | |
| TC-C-08 | Apply coupon at max usage limit (D-U2, on point) | `{code:"SAVE10", total_amount:500000, user_id:1}` | 1 prior use, max=1 | POST /api/apply-coupon | Error: usage limit reached | | |
| TC-C-09 | Apply percent coupon — observe discount_value bug | `{code:"SAVE10", total_amount:500000, user_id:1}` | SAVE10 discount_value=10 (integer) | POST /api/apply-coupon | Bug: `final = 500000 * (1-10) = -4,500,000` instead of 450,000 | | |
| TC-C-10 | Apply fixed coupon correctly | `{code:"BIGBUY", total_amount:600000, user_id:1}` | BIGBUY: fixed 50000 off, min=500000 | POST /api/apply-coupon | 200, final_amount = 550,000 | | |
| TC-C-11 | Delete existing coupon | `id` of created coupon | Admin logged in | DELETE /api/admin/coupons/:id | 200 "Coupon deleted" | | |
| TC-C-12 | Create coupon with invalid type (D-T3) | `{code:"BAD1", type:"cashback", ...}` | Admin logged in | POST /api/admin/coupons | Should reject invalid type; no validation → silently stored (bug) | | |
| TC-C-13 | Apply VIP100 coupon — multiple uses (max=2) | `{code:"VIP100", total_amount:400000, user_id:1}` | 0 prior uses, max=2 | Apply twice | First and second application succeed; third rejected | | |

### 4.2 Boundary Value Analysis

_[To be filled]_

### 4.3 AI Gap Analysis

_[To be filled after test execution]_

### 4.4 Bug Report

| Bug ID | Title | Severity | Steps to Reproduce | Expected | Actual | GitHub Issue |
|--------|-------|----------|--------------------|----------|--------|--------------|

---

## 5. Feature D — Mobile App (Pool D)

### 5.1 Domain Testing

#### Step-by-step Technique Application

**Step 1 — Understand the feature from source code**

The mobile app (`frontend-mobile/App.js`) is a React Native application. The key feature with rich domain behavior is the **product quantity input and cart management**:

Key functions:
```javascript
const normalizeQuantity = (value) => {
  const parsed = parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
};
```
Cart item inline edit (line 617):
```javascript
const parsed = parseInt(text, 10);
newCart[index].quantity = isNaN(parsed) || parsed < 1 ? 1 : parsed;
```

Checkout total calculation:
```javascript
const cartTotal = cart.reduce((total, item) => total + item.price * item.quantity, 0);
```

Key observations:
1. `normalizeQuantity`: silently converts any invalid/zero/negative quantity to `1`.
2. No upper bound on quantity — can add 999,999 items.
3. No stock check — product stock is not tracked.
4. Cart is pure in-memory (React state) — resets on app restart.
5. Login: same backend endpoint as FR-02 (email + password).

**Step 2 — Identify input variables**

| Variable | Screen | Domain concern |
|----------|--------|----------------|
| `quantity` (product detail) | Product Detail | String input → parseInt; silent normalization |
| `quantity` (cart edit) | Cart screen | Direct edit; similar normalization |
| `email` (login) | Login | Same as FR-02 |
| `password` (login) | Login | Same as FR-02 |
| `couponCode` (cart) | Cart screen | Uppercase-trimmed before sending |

**Step 3 — Define domains for `quantity` input (primary mobile domain)**

| Domain | Class | Representative |
|--------|-------|----------------|
| D-Q1 | Valid: positive integer string ≥ 1 | `"1"`, `"5"`, `"99"` |
| D-Q2 | Invalid: zero string | `"0"` → normalized to 1 |
| D-Q3 | Invalid: negative string | `"-1"`, `"-5"` → normalized to 1 |
| D-Q4 | Invalid: float string | `"1.5"` → parseInt gives 1 |
| D-Q5 | Invalid: alphabetic string | `"abc"` → NaN → normalized to 1 |
| D-Q6 | Invalid: empty string | `""` → NaN → normalized to 1 |
| D-Q7 | Edge: very large integer | `"99999"` → accepted (no upper limit) |
| D-Q8 | Edge: leading zeros | `"007"` → parseInt gives 7 |

**Step 4 — Identify boundary points**

| Variable | Boundary | On Point | Off Point | In Point | Out Point |
|----------|----------|----------|-----------|----------|-----------|
| quantity (normalizeQuantity: `parsed > 0`) | `parsed > 0` | `1` (just valid, kept) | `0` (just below, → 1) | `5` | `-1` (→ 1) |
| quantity (cart inline edit: `parsed < 1`) | `parsed >= 1` | `1` | `0` (→ 1) | `3` | `"abc"` (→ 1) |
| quantity upper limit | none defined | no upper bound | N/A | `99` | none rejected |

**Step 5 — Design test cases**

---

#### Test Cases

| TC ID | Objective | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-D-01 | Add product with quantity=1 (on point, D-Q1) | Quantity = `"1"` | Product detail screen open | Enter "1", tap Add to Cart | Cart shows product with quantity=1 | | |
| TC-D-02 | Add product with quantity=5 (in point, D-Q1) | Quantity = `"5"` | Product detail screen | Enter "5", tap Add to Cart | Cart shows product with quantity=5 | | |
| TC-D-03 | Add product with quantity=0 (off point, D-Q2) | Quantity = `"0"` | Product detail screen | Enter "0", tap Add to Cart | normalizeQuantity → quantity=1; item added with qty=1 (silent normalization, no warning) | | |
| TC-D-04 | Add product with negative quantity (D-Q3) | Quantity = `"-3"` | Product detail screen | Enter "-3", tap Add to Cart | normalizeQuantity → 1; no error shown to user | | |
| TC-D-05 | Add product with float quantity (D-Q4) | Quantity = `"2.9"` | Product detail screen | Enter "2.9", tap Add to Cart | parseInt("2.9")=2; item added with qty=2 (truncated, no warning) | | |
| TC-D-06 | Add product with alphabetic quantity (D-Q5) | Quantity = `"abc"` | Product detail screen | Enter "abc", tap Add to Cart | NaN → normalized to 1; item added with qty=1 | | |
| TC-D-07 | Add product with empty quantity (D-Q6) | Quantity = `""` | Product detail screen | Clear input, tap Add to Cart | NaN → normalized to 1 | | |
| TC-D-08 | Add product with very large quantity (D-Q7) | Quantity = `"99999"` | Product detail screen | Enter "99999", tap Add to Cart | Accepted with qty=99999; no upper bound validation | | |
| TC-D-09 | Edit quantity in cart to 0 (off point) | Inline cart edit → `"0"` | Item in cart | Edit quantity field to "0" | `parsed < 1` → quantity set to 1; no error message | | |
| TC-D-10 | Login with valid credentials (mobile) | email: `test@eshop.com`, password: `Test1234!` | App on login screen | Enter credentials, tap Login | Navigates to product list; JWT stored | | |
| TC-D-11 | Login with wrong password (mobile, D-P2) | email: `test@eshop.com`, password: `wrong` | App on login screen | Enter wrong password | Error message shown: "Invalid email or password" | | |
| TC-D-12 | Apply coupon in mobile cart | couponCode = `"save10"` (lowercase) | Items in cart, total ≥ 300001 | Enter "save10" in coupon field, tap Apply | Code uppercased to "SAVE10" before API call; discount applied | | |
| TC-D-13 | Coupon code with whitespace | couponCode = `"  SAVE10  "` | Items in cart | Enter padded code | `.trim()` removes spaces; "SAVE10" sent to API | | |
| TC-D-14 | Cart total calculation with multiple items | Item A: price=100000 qty=2; Item B: price=50000 qty=3 | Empty cart | Add both items | Total = 100000×2 + 50000×3 = 350,000 | | |

### 5.2 Boundary Value Analysis

_[To be filled]_

### 5.3 AI Gap Analysis

_[To be filled after test execution]_

### 5.4 Bug Report

| Bug ID | Title | Severity | Steps to Reproduce | Expected | Actual | GitHub Issue |
|--------|-------|----------|--------------------|----------|--------|--------------|

---

## 6. AI Critique

_(200–300 words — fill in with /ai-critique skill)_

<!-- Target: 200–300 words. Cover:
  1. Where the AI was wrong or incomplete (be specific — name the artifact and error)
  2. Why the AI failed (training limits, no physical access, etc.)
  3. At least one concrete bias or hallucination found
  4. One actionable principle learned for AI collaboration on testing work
  Include word count at the end. -->

---

## 7. Mandatory Disclosure

_(Fill in with /disclosure skill)_

> "[artifact(s)] was initially generated by [AI tool name]; I reviewed and modified [section X], added [edge cases Y, Z]; [section W] was written entirely by me. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category below."

**I confirm I did NOT use AI to generate:**
- [ ] Bug screenshots
- [ ] Execution/demo videos (recorded with my own voice narration)
- [ ] Prompt log entries (real prompts with real timestamps)

---

## 8. Appendix A — Prompt Log

_(See `report/appendix_A_prompt_log.md`)_
