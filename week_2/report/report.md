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

> **UI Observation (black-box):** The login screen labels the first field as **"Username"** (not "Email"). Based on observable behaviour with test data, the system accepts email-format strings in this field. All test case inputs reference it as `username`. Also observed: the page title displays **"Đăng Ký"** (Register) on the login page — this is a suspected UI bug (should read "Đăng Nhập" / Sign In).

| Variable | Type | Description |
|----------|------|-------------|
| `username` | string | Account identifier — UI field labeled "Username"; accepts email-format strings |
| `password` | string | Credential — UI field labeled "Mật khẩu" |
| `account_state` | derived | Observed state: clean / failed-attempt / locked / lock-expired |

**Step 3 — Define domains (equivalence classes) for each variable**

**Variable: `username`** *(UI label: "Username"; accepts email-format strings)*
| Domain | Class | Representative Value |
|--------|-------|----------------------|
| D-E1 | Valid: registered username (email-format) | `test@eshop.com` |
| D-E2 | Invalid: unregistered, well-formed email-format | `nobody@eshop.com` |
| D-E3 | Invalid: non-email-format string (no `@`) — treated as unregistered username, **not** a format error | `testeshop.com`, `johndoe` |
| D-E4 | Invalid: empty string | `""` |
| D-E5 | Invalid: null / missing field | `null` |
| D-E6 | Edge: username with leading/trailing whitespace | `" test@eshop.com "` |
| D-E7 | Edge: injection-attempt string | `' OR 1=1 --` |
| D-E8 | Malformed: multiple `@` symbols (RFC 5321 violation) | `test@@eshop.com` |
| D-E9 | Malformed: missing domain after `@` | `test@` |
| D-E10 | Malformed: missing local part before `@` | `@eshop.com` |
| D-E11 | Malformed: no TLD in domain (RFC 5321 violation) | `test@eshop` |
| D-E12 | Malformed: space within string | `test @eshop.com` |
| D-E13 | Malformed: consecutive dots in local part | `test..user@eshop.com` |
| D-E14 | Malformed: local part starts with dot | `.test@eshop.com` |
| D-E15 | Boundary: string exceeds RFC 5321 max (254 chars) | 255-char email string |

> **RFC 5321 constraints (best practice):** max total email length = 254 chars; local part max = 64 chars; domain labels separated by dots; no consecutive dots; local part cannot start or end with a dot.

**Variable: `password`**
| Domain | Class | Representative Value |
|--------|-------|----------------------|
| D-P1 | Valid: correct password for the account | `Test1234!` |
| D-P2 | Invalid: wrong password (non-empty string) | `WrongPass99` |
| D-P3 | Invalid: empty string | `""` |
| D-P4 | Invalid: null / missing field | `null` |
| D-P5 | Edge: whitespace-only string | `"   "` |
| D-P6 | Edge: correct password with different case | `TEST1234!` (if stored as `Test1234!`) |
| D-P7 | Boundary: below NIST SP 800-63B minimum (< 8 chars) | `Pass12!` (7 chars) |
| D-P8 | Boundary: at NIST SP 800-63B minimum (8 chars) | `Pass1234` |
| D-P9 | Boundary: exceeds NIST recommended max (> 64 chars) | 65-char password string |
| D-P10 | Edge: Unicode / multibyte characters | `Pässwörð!1` |
| D-P11 | Security: password field visible (type="text" bug) | Inspect rendered input type attribute |

> **NIST SP 800-63B constraints (best practice):** minimum 8 characters; support at least 64 characters; allow all ASCII and Unicode; password field MUST use `type="password"` to mask input.

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
| TC-A-01 | Valid login (clean account) | username: `test@eshop.com`, password: `Test1234!` | Account clean (`login_attempts=0`) | Enter credentials in UI, click Sign In | 200 OK, redirected to product list | Redirected to `/` (home page); login successful | ✅ PASS |
| TC-A-02 | Unregistered username — email-format (D-E2) | username: `nobody@eshop.com`, password: `Test1234!` | N/A | Enter credentials, click Sign In | 401 "Invalid email or password" | Error banner: "Đăng nhập thất bại. Vui lòng kiểm tra lại."; remains on `/login` | ✅ PASS |
| TC-A-03 | Non-email-format username (D-E3) | username: `testeshop.com`, password: `Test1234!` | N/A | Enter credentials, click Sign In | 401 "Invalid email or password" — UI shows "Username" field, so no email-format validation is expected; any unregistered string returns 401 | Same generic error; no format validation performed | ✅ PASS |
| TC-A-04 | Empty username (D-E4) | username: `""`, password: `Test1234!` | N/A | Leave username blank, click Sign In | 401 or inline "required field" error | HTML5 `required` attribute fires; browser blocks submission; stays on `/login` | ✅ PASS |
| TC-A-05 | Missing username field (D-E5) | No username value, password: `Test1234!` | N/A | Submit form without username | 401 or 400 error | HTML5 `required` blocks submission; stays on `/login` | ✅ PASS |
| TC-A-06 | Wrong password — 1st attempt (D-P2, off point: newAttempts=2) | username: `test@eshop.com`, password: `WrongPass99` | `login_attempts=0` | Enter wrong password, click Sign In | 401 error; account NOT locked | Error shown; account remains accessible for retry (not locked) | ✅ PASS |
| TC-A-07 | Wrong password — 2nd attempt (on point: triggers lockout) | username: `test@eshop.com`, password: `WrongPass99` | 1 prior failure (after TC-A-06) | Enter wrong password, click Sign In | 401 error; account LOCKED for 3 minutes | Error shown; subsequent attempt with correct password also fails — account locked | ✅ PASS |
| TC-A-08 | Login while actively locked (D-S3) | username: `test@eshop.com`, password: `Test1234!` | Account locked (`locked_until` in future) | Enter correct credentials, click Sign In | 403 "Tài khoản đã bị khóa. Vui lòng thử lại sau." | Error shown; correct credentials rejected while locked. Note: UI shows generic "Đăng nhập thất bại…" — does not expose lock-specific message | ✅ PASS |
| TC-A-09 | Login after lock expires (D-S4) | username: `test@eshop.com`, password: `Test1234!` | `locked_until` set to past timestamp | Enter correct credentials after 3+ minutes | 200 OK, login success; lock ignored | Redirected to home; expired lock does not block login | ✅ PASS |
| TC-A-10 | Correct password after 1 failed attempt (D-S2) | username: `test@eshop.com`, password: `Test1234!` | 1 prior failure (not locked) | Enter correct credentials, click Sign In | 200 OK; failed-attempt counter reset to 0 | Redirected to home; login successful | ✅ PASS |
| TC-A-11 | Empty password (D-P3) | username: `test@eshop.com`, password: `""` | Clean account | Leave password blank, click Sign In | 401 "Invalid email or password" | HTML5 `required` blocks submission; stays on `/login` | ✅ PASS |
| TC-A-12 | Missing password field (D-P4) | username: `test@eshop.com`, no password | Clean account | Submit without password | 401 or 400 error | HTML5 `required` blocks submission | ✅ PASS |
| TC-A-13 | Pure alphanumeric username — no @ (D-E3, black-box) | username: `johndoe`, password: `Test1234!` | N/A | Enter `johndoe` in Username field, click Sign In | 401 "Invalid email or password" — system treats any unregistered string uniformly, regardless of format | Generic error shown; no format discrimination | ✅ PASS |
| TC-A-14 | Username with leading/trailing whitespace (D-E6) | username: `" test@eshop.com "`, password: `Test1234!` | Registered account is `test@eshop.com` | Enter padded username, click Sign In | Observable: either 200 OK (whitespace trimmed by system) or 401 (whitespace preserved — no match) | **401 — whitespace NOT trimmed;** `" test@eshop.com "` does not match stored `test@eshop.com` | ✅ PASS (behavior documented) |
| TC-A-15 | Injection-attempt string in username (D-E7) | username: `' OR 1=1 --`, password: `Test1234!` | N/A | Enter injection string, click Sign In | 401 — system must not authenticate or crash; safe rejection expected | Generic 401 error; no injection; DB uses parameterized queries | ✅ PASS |
| TC-A-16 | Password case sensitivity (D-P6) | username: `test@eshop.com`, password: `TEST1234!` | Registered password is `Test1234!` | Enter password with wrong case, click Sign In | 401 — password comparison is case-sensitive; wrong case = wrong password | Error shown; password comparison is case-sensitive (plain-text `===` comparison) | ✅ PASS |
| TC-A-17 | Whitespace-only password (D-P5) | username: `test@eshop.com`, password: `"   "` | Clean account | Enter 3 spaces as password, click Sign In | 401 "Invalid email or password" | Error shown; 3-space password treated as wrong password | ✅ PASS |
| TC-A-18 | Both fields empty (boundary combination) | username: `""`, password: `""` | N/A | Leave both fields blank, click Sign In | Error: both fields required, or 401 — no authentication should occur | HTML5 `required` fires for both fields; form blocked; no authentication | ✅ PASS |
| TC-A-19 | UI — page title mismatch (observed bug) | N/A | N/A | Navigate to the login page | **Expected:** Page title reads "Đăng Nhập" (Sign In). **Observed:** Title reads "Đăng Ký" (Register) — UI defect | `h2` reads `"Đăng Ký"` (Register) — confirmed UI bug. Login.jsx has mis-labeled title. **→ BUG-A-01** | ❌ FAIL |
| TC-A-20 | Password field masking — security constraint (D-P11) | N/A | N/A | Inspect password input `type` attribute on login page | **Expected:** `type="password"` (characters masked). **Best-practice violation if `type="text"`** — password visible in plaintext | Password input `type="text"` — password visible in plaintext. **→ BUG-A-02** | ❌ FAIL |

#### Constraint-based Test Cases (RFC 5321 / NIST SP 800-63B best practices)

> These test cases cover constraints derived from industry standards, independent of what the current implementation validates.

| TC ID | Constraint Standard | Objective | Input | Pre-condition | Steps | Expected (best practice) | Actual Result | Verdict |
|-------|-------------------|-----------|-------|---------------|-------|--------------------------|---------------|---------|
| TC-A-C-01 | RFC 5321 | Multiple `@` symbols (D-E8) | username: `test@@eshop.com`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 "Invalid email format". Current: 401 (no format validation) | Generic error "Đăng nhập thất bại…"; no auth. No format-specific message | ⚠️ PASS* |
| TC-A-C-02 | RFC 5321 | Missing domain after `@` (D-E9) | username: `test@`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 "Invalid email format". Current: 401 | Generic 401 error; no auth. No format-specific message | ⚠️ PASS* |
| TC-A-C-03 | RFC 5321 | Missing local part before `@` (D-E10) | username: `@eshop.com`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 "Invalid email format". Current: 401 | Generic 401 error; no auth | ⚠️ PASS* |
| TC-A-C-04 | RFC 5321 | No TLD in domain (D-E11) | username: `test@eshop`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 "Invalid email format" — a valid domain must have a TLD. Current: 401 | Generic 401 error; no auth | ⚠️ PASS* |
| TC-A-C-05 | RFC 5321 | Space within username (D-E12) | username: `test @eshop.com`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 — spaces are not valid in email addresses. Current: 401 | Generic 401 error; no auth | ⚠️ PASS* |
| TC-A-C-06 | RFC 5321 | Consecutive dots in local part (D-E13) | username: `test..user@eshop.com`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 "Invalid email format". Current: 401 | Generic 401 error; no auth | ⚠️ PASS* |
| TC-A-C-07 | RFC 5321 | Local part starts with dot (D-E14) | username: `.test@eshop.com`, password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400. Current: 401 | Generic 401 error; no auth | ⚠️ PASS* |
| TC-A-C-08 | RFC 5321 | Total email length at RFC max (254 chars) | username: `${"a"×244}@eshop.com` (254 chars), password: `Test1234!` | N/A | Enter, click Sign In | 401 (not registered — but format is valid per RFC) | Generic 401; system accepts 254-char length without error | ✅ PASS |
| TC-A-C-09 | RFC 5321 | Total email length exceeds RFC max (255 chars) (D-E15) | username: `${"a"×245}@eshop.com` (255 chars), password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400/413 — reject input exceeding 254 chars. Current: 401 (no length check) | Generic error: "Đăng nhập thất bại…"; no length-specific rejection | ⚠️ PASS* |
| TC-A-C-10 | RFC 5321 | Local part exceeds 64 chars | username: `${"a"×65}@eshop.com` (65 chars before @), password: `Test1234!` | N/A | Enter, click Sign In | **Best practice:** 400 — local part must not exceed 64 chars. Current: 401 | Generic error: "Đăng nhập thất bại…"; no format-specific message | ⚠️ PASS* |
| TC-A-C-11 | NIST 800-63B | Password below minimum length (7 chars) (D-P7) | username: `test@eshop.com`, password: `Pass12!` | Clean account | Enter, click Sign In | **Best practice:** 400 "Password too short (min 8 chars)". Current: 401 (no length check) | Generic error: "Đăng nhập thất bại…"; no min-length enforcement | ⚠️ PASS* |
| TC-A-C-12 | NIST 800-63B | Password at minimum length (8 chars) (D-P8) | username: `test@eshop.com`, password: `Pass1234` | Clean account | Enter, click Sign In | 401 (wrong password, but format valid per NIST min) | Generic 401; no crash; 8-char passwords handled correctly | ✅ PASS |
| TC-A-C-13 | NIST 800-63B | Password exceeds recommended max (65 chars) (D-P9) | username: `test@eshop.com`, password: `${"A"×65}` | Clean account | Enter, click Sign In | System should support ≥ 64 chars without truncating or crashing. 401 (wrong) | Generic 401; no crash or truncation error — NIST ≥ 64 char support confirmed | ✅ PASS |
| TC-A-C-14 | NIST 800-63B | Password with Unicode characters (D-P10) | username: `test@eshop.com`, password: `Pässwörð!1` | Clean account | Enter, click Sign In | 401 (wrong password); system must not crash on multibyte input | Generic 401; no crash on Unicode input | ✅ PASS |
| TC-A-C-15 | OWASP / Security | XSS attempt in username | username: `<script>alert(1)</script>`, password: `Test1234!` | N/A | Enter, click Sign In | 401; no alert dialog appears; input safely escaped | Generic 401; no alert dialog; input safely handled | ✅ PASS |
| TC-A-C-16 | OWASP / Security | XSS attempt in password | username: `test@eshop.com`, password: `<img src=x onerror=alert(1)>` | N/A | Enter, click Sign In | 401; no script/alert executes | Generic 401; no alert dialog; input safely handled | ✅ PASS |

> ⚠️ **PASS\* note:** These tests pass in the sense that **no authentication bypass or crash occurred**. However, they reveal a compliance gap: the system returns a generic error instead of a standards-compliant format or length error message. This is a usability and security-hardening defect.

### 2.2 Boundary Value Analysis

#### Step-by-step Technique Application

**Step 1 — Identify variables with testable boundaries**

BVA applies to variables whose valid/invalid partition has an ordered, measurable boundary. Six variables qualify:

| Variable | Observable Range | Key Boundary |
|----------|-----------------|--------------|
| Failed login attempts | 0 → lockout | Threshold N where account locks |
| Lock duration | 0 → ~3 min | Expiry moment (locked vs unlocked) |
| Username string length | 0 chars → ∞ | Empty (0 chars) vs non-empty; RFC 5321 max (254 chars) |
| Username local-part length | 0 → ∞ | RFC 5321 local-part max (64 chars) |
| Password string length | 0 chars → ∞ | Empty; NIST min (8 chars); NIST recommended max (64 chars) |
| Lock expiry timestamp | past → future | `locked_until` vs `now` |

---

**Step 2 — Determine boundary points**

**Variable 1: Failed attempts vs lockout threshold**

From observed behaviour (TC-A-06, TC-A-07): the account locks on the **2nd** consecutive wrong-password attempt.

| BVA Point | Description | State |
|-----------|-------------|-------|
| In point | 0 failures — clean account | No lock risk |
| Off point (below threshold) | 1 failure — just safe | 401 returned; account still open |
| On point (threshold) | 2nd failure — lockout triggered | 401 returned; account now locked |
| Out point (beyond threshold) | Any attempt while locked | 403 returned regardless of password |

> ⚠️ **Anomaly**: Lockout on attempt 2 (not attempt 3) indicates a boundary skip — consistent with a +2 increment defect. The threshold value 3 is never actually reached; the counter jumps from 2 → 4. This is an observable black-box abnormality worth explicitly testing.

**Variable 2: Lock duration (~3 minutes = 180 seconds)**

| BVA Point | Time after lockout | Description |
|-----------|-------------------|-------------|
| In point | ~60 s | Well inside lock window |
| Off point (1 s before expiry) | 179 s | Still locked |
| On point (at expiry) | 180 s | Boundary — locked_until condition transitions |
| Out point (1 s after expiry) | 181 s | Lock expired; login should succeed |

**Variable 3: Username string length**

| BVA Point | Length | Value |
|-----------|--------|-------|
| Off point | 0 chars | `""` (empty) |
| On point | 1 char | `"a"` |
| In point | Typical | `"test@eshop.com"` |

**Variable 4: Password string length**

| BVA Point | Length | Value |
|-----------|--------|-------|
| Off point | 0 chars | `""` (empty) |
| On point | 1 char | `"X"` |
| In point | Typical | `"Test1234!"` |

---

**Step 3 — Design BVA test cases** (one variable varied at a time; others at in-point)

#### BVA Test Cases

| TC ID | Variable | BVA Point | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|----------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-A-BV-01 | Failed attempts | In point (0 failures → 1st wrong attempt) | username: `test@eshop.com`, password: `WrongPass99` | Clean account (0 prior failures) | Enter wrong password, click Sign In | 401 error message; account NOT locked; can retry | Error shown; can attempt again (not locked) | ✅ PASS |
| TC-A-BV-02 | Failed attempts | Off point (1 failure — just below lockout threshold) | username: `test@eshop.com`, password: `WrongPass99` | 1 prior failure (account still open) | Enter wrong password again | 401 error; account NOT YET locked | Correct password accepted after 1 failure (login_attempts=2 < 3); not locked | ✅ PASS |
| TC-A-BV-03 | Failed attempts | On point (threshold attempt — triggers lockout) | username: `test@eshop.com`, password: `WrongPass99` | State is exactly 1 attempt below lockout | Enter wrong password | 401; AND account is NOW locked | 2nd wrong attempt (login_attempts: 2→4 ≥ 3) triggers lock; correct password then rejected | ✅ PASS |
| TC-A-BV-04 | Failed attempts | Out point (attempt while already locked) | username: `test@eshop.com`, password: `Test1234!` *(correct)* | Account locked after TC-A-BV-03 | Enter correct password immediately | 403 "Tài khoản đã bị khóa…" — correct credentials rejected while locked | Correct credentials rejected; generic error displayed | ✅ PASS |
| TC-A-BV-05 | Lock duration | In point (~2 s into 3-min lock) | username: `test@eshop.com`, password: `Test1234!` | Account locked 2 s ago | Wait 2 s, click Sign In | 403; still locked | Error shown; ~177 s remain; still locked | ✅ PASS |
| TC-A-BV-06 | Lock duration | Off point (1 s before expiry) | username: `test@eshop.com`, password: `Test1234!` | `locked_until = now + 3s`; wait 2s | Attempt at t=2 s (1 s remaining) | 403; still locked | Error shown; lock still active 1 s before expiry | ✅ PASS |
| TC-A-BV-07 | Lock duration | On point (at expiry boundary) | username: `test@eshop.com`, password: `Test1234!` | `locked_until = now + 3s`; wait 4s | Attempt at t=4 s (1 s past expiry) | 200 OK or 403 depending on `>` vs `>=` | **Login SUCCEEDS** — server uses strict `locked_until > now`; at expiry moment lock is released | ✅ PASS |
| TC-A-BV-08 | Lock duration | Out point (after expiry) | username: `test@eshop.com`, password: `Test1234!` | `locked_until` set 5 s in the past | Attempt login | 200 OK; lock expired, login succeeds | Redirected to home; expired lock does not block | ✅ PASS |
| TC-A-BV-09 | Username length | Off point (0 chars — empty) | username: `""`, password: `Test1234!` | N/A | Leave username blank, click Sign In | Error: required field or 401 | HTML5 `required` blocks form; stays on `/login` | ✅ PASS |
| TC-A-BV-10 | Username length | On point (1 char) | username: `"a"`, password: `Test1234!` | N/A | Enter `a`, click Sign In | 401 (not registered) | Generic 401 error | ✅ PASS |
| TC-A-BV-11 | Password length | Off point (0 chars — empty) | username: `test@eshop.com`, password: `""` | Clean account | Leave password blank, click Sign In | Error: required field or 401 | HTML5 `required` blocks form | ✅ PASS |
| TC-A-BV-12 | Password length | On point (1 char — wrong) | username: `test@eshop.com`, password: `"X"` | Clean account | Enter 1-char password, click Sign In | 401; counter incremented | Generic 401 error | ✅ PASS |
| TC-A-BV-13 | Lockout counter reset | Boundary: successful login resets counter | username: `test@eshop.com`, password: `Test1234!` | 1 prior failure (not locked) | Enter correct password, click Sign In | 200 OK; counter reset to 0 | Login succeeds; subsequent single wrong attempt does not immediately lock | ✅ PASS |
| TC-A-BV-14 | Username total length | Off point below RFC max (253 chars) | 253-char email, password: `Test1234!` | N/A | Enter, click Sign In | 401 (within RFC limit; not registered) | Generic 401; no length error | ✅ PASS |
| TC-A-BV-15 | Username total length | On point at RFC max (254 chars) | 254-char email, password: `Test1234!` | N/A | Enter, click Sign In | 401 (RFC-valid length; not registered) | Generic 401; 254-char email accepted | ✅ PASS |
| TC-A-BV-16 | Username total length | Out point above RFC max (255 chars) | 255-char email, password: `Test1234!` | N/A | Enter, click Sign In | Best practice: 400/413 reject > 254 chars | Generic "Đăng nhập thất bại…" error; **no RFC length enforcement** — compliance gap | ⚠️ PASS* |
| TC-A-BV-17 | Local-part length | On point at RFC max (64 chars before @) | `"a"×64 + "@eshop.com"`, password: `Test1234!` | N/A | Enter, click Sign In | 401 (RFC-valid; not registered) | Generic 401; 64-char local part accepted | ✅ PASS |
| TC-A-BV-18 | Local-part length | Out point above RFC max (65 chars before @) | `"a"×65 + "@eshop.com"`, password: `Test1234!` | N/A | Enter, click Sign In | Best practice: 400 format error | Generic 401 error; **no local-part length enforcement** — compliance gap | ⚠️ PASS* |
| TC-A-BV-19 | Password length | Off point below NIST min (7 chars) | password: `Pass12!` (7 chars) | Clean account | Enter, click Sign In | Best practice: 400 "min 8 chars" | Generic 401; **no NIST min-length enforcement** | ⚠️ PASS* |
| TC-A-BV-20 | Password length | On point at NIST min (8 chars) | password: `Pass1234` (8 chars) | Clean account | Enter, click Sign In | 401 (wrong; length valid per NIST) | Generic 401; no crash | ✅ PASS |
| TC-A-BV-21 | Password length | On point at NIST recommended max (64 chars) | password: `"A"×64` | Clean account | Enter, click Sign In | 401; no crash or truncation | Generic 401; 64-char password handled correctly | ✅ PASS |
| TC-A-BV-22 | Password length | Out point above NIST max (65 chars) | password: `"A"×65` | Clean account | Enter, click Sign In | 401; NIST requires ≥ 64 char support; no crash | Generic 401; 65-char password handled without crash | ✅ PASS |

### 2.3 AI Gap Analysis

**Bugs and gaps the AI initially missed or under-specified:**

1. **Password field type bug (TC-A-20)** — The AI's initial domain analysis focused entirely on credential logic and never considered that the password input field itself might be `type="text"` instead of `type="password"`. This is an elementary UI security defect that only became visible when the screenshot was provided and the JSX source was checked. The AI did not proactively test UI security properties.

2. **Page title mismatch (TC-A-19)** — The AI correctly noted this from the screenshot, but would not have identified it without the visual artefact. Text-only code inspection misses presentational bugs in the rendered DOM.

3. **RFC 5321 format constraints (TC-A-C-01–10)** — The AI's original domain analysis only checked "valid email", "unregistered email", and "no @" cases. It did not enumerate individual RFC 5321 sub-rules (consecutive dots, leading dots, missing TLD, multiple @). These were only added after the user explicitly asked for best-practice constraints.

4. **NIST password length boundaries (TC-A-C-11, TC-A-BV-19–22)** — BVA initially only identified the "empty vs non-empty" length boundary. The NIST SP 800-63B minimum of 8 characters and the recommended max of 64 characters were only incorporated after the user pushed for standard-based constraints.

5. **Generic UI error message gap** — The AI test assertions initially expected the backend's HTTP 401/403 error messages verbatim. The actual UI always shows the generic string `"Đăng nhập thất bại. Vui lòng kiểm tra lại."` regardless of error type, because Login.jsx swallows all errors. This means locked-account users get no actionable feedback — a UX defect the AI did not flag.

**Why the AI missed these:**
- The AI had no visual access to the running application; it reasoned from source code alone.
- It applied standard equivalence partitioning without referencing industry standards (RFC 5321, NIST 800-63B) until prompted.
- It did not treat UI attribute correctness (input `type`, `h2` text) as testable assertions until the screenshot provided evidence.

### 2.4 Bug Report

| Bug ID | Title | Severity | Steps to Reproduce | Expected | Actual | GitHub Issue |
|--------|-------|----------|--------------------|----------|--------|--------------|
| BUG-A-01 | Login page title shows "Đăng Ký" (Register) instead of "Đăng Nhập" (Sign In) | Low | Navigate to `/login` | Page `h2` heading reads "Đăng Nhập" (Sign In) | `h2` reads "Đăng Ký" (Register) — wrong label | |
| BUG-A-02 | Password input field uses `type="text"` — password visible in plaintext | **High (Security)** | 1. Navigate to `/login`. 2. Observe the "Mật khẩu" field. 3. Type any password | Password characters masked (`type="password"`) | Characters visible in plaintext; any shoulder-surfing or screen recording exposes passwords (`type="text"` in Login.jsx line 39) | |
| BUG-A-03 | `login_attempts` incremented by 2 per failure — lockout triggers on attempt 2 not 3 | **High** | 1. Enter wrong password twice with the same account. 2. Observe account locked after 2nd attempt | Account should lock after 3 consecutive failures | `newAttempts = user.login_attempts + 2` (server.js line 54); after attempt 1: attempts=2, attempt 2: attempts=4 ≥ 3 → locked. Threshold value of 3 is never reached — boundary skipped | |
| BUG-A-04 | No RFC 5321 email format validation — malformed emails accepted as input | Medium | Submit malformed email values: `test@@eshop.com`, `test@`, `@eshop.com`, `.test@eshop.com`, `test..user@eshop.com` | 400 "Invalid email format" with specific validation message | Generic 401 "Đăng nhập thất bại…" for all malformed formats; server performs no format validation before DB lookup | |
| BUG-A-05 | No NIST SP 800-63B password minimum length enforcement — 1-char passwords accepted | Medium | Submit password `"X"` (1 char) or `"Pass12!"` (7 chars) at login | Best practice: reject passwords shorter than 8 characters with explicit error | Generic 401; no length check; 1-char passwords processed without error | |
| BUG-A-06 | Login error message does not distinguish wrong credentials from account lockout | Medium | 1. Lock an account. 2. Attempt login with correct credentials | Distinct error: "Account locked, try again after X minutes" | Same generic "Đăng nhập thất bại. Vui lòng kiểm tra lại." shown for both wrong password and locked account — user cannot distinguish the cause | |

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
| `price` | integer | Taken from product data — but **fully user-controllable via API** since POST /api/cart pushes any body object with no server-side validation |
| `total_amount` | integer | Passed at checkout — **not server-verified** against actual cart contents |
| `shipping_address` | string | User input at checkout |
| `auth_state` | derived | Observed state: authenticated (valid token) / unauthenticated (no/invalid token) |

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
| D-Q7 | Edge: extremely large integer | `999999`, `2147483647` (INT_MAX) |

> ⚠️ **Note on server behaviour:** POST /api/cart has **no server-side quantity validation**. D-Q2 through D-Q6 are all *accepted* by the server — these tests confirm the bug, they do not test rejection.

**Variable: `price` (POST /api/cart body — user-controllable via API)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-PR1 | Valid: positive integer | `100000`, `500000` |
| D-PR2 | Invalid: zero price | `0` |
| D-PR3 | Invalid: negative price | `-100000` |
| D-PR4 | Invalid: non-numeric | `"free"` |

> ⚠️ **Security note:** Since the server pushes any body object directly, a client can supply an arbitrary `price` value (e.g., `1`). The cart total is then calculated as `price × quantity` — enabling price manipulation.

**Variable: `total_amount` (POST /api/checkout)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-T1 | Valid: positive integer > 0 | `100000`, `500000` |
| D-T2 | Invalid: zero | `0` |
| D-T3 | Invalid: negative | `-100000` |
| D-T4 | Invalid: non-numeric | `"abc"` |
| D-T5 | Invalid: null / missing | `null` |

> ⚠️ **Note on server behaviour:** POST /api/checkout does **not verify** `total_amount` against the cart's computed total. Any numeric value is accepted.

**Variable: `shipping_address` (POST /api/checkout)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-A1 | Valid: non-empty string | `"123 Le Loi, Q1, TP.HCM"` |
| D-A2 | Invalid: empty string | `""` |
| D-A3 | Invalid: null / missing | `null` |
| D-A4 | Edge: very long string (> 500 chars) | 501-char address string |
| D-A5 | Security: XSS payload | `"<script>alert(1)</script>"` |

**Variable: `auth_state` (all cart/checkout endpoints)**
| Domain | Class | Representative |
|--------|-------|----------------|
| D-Auth1 | Valid: authenticated user | User logged in; valid session token present |
| D-Auth2 | Invalid: unauthenticated | No token / expired token |

**Step 4 — Identify boundary points**

| Variable | Boundary | On Point | Off Point | In Point | Out Point |
|----------|----------|----------|-----------|----------|-----------|
| `quantity` (mobile normalizeQuantity: `> 0`) | `parsed > 0` | `1` (just valid) | `0` (just invalid → normalized to 1) | `5` | `-1` |
| `quantity` (extreme upper) | No server upper limit defined | `999999` (accepted) | N/A | `5` | N/A (no cap) |
| `total_amount` at checkout | `> 0` (no server enforcement) | `1` | `0` | `100000` | `-1` |
| `shipping_address` length | Non-empty required | `1 char` | `0 chars` (`""`) | `"123 Le Loi"` | `null` |

**Step 5 — Design test cases**

---

#### Test Cases

| TC ID | Objective | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-B-01 | Add item with valid quantity (D-Q1, in point) | `{id:1, name:"X", price:100000, quantity:5}` | Logged in | POST /api/cart | 200 "Added to cart"; cart has item with quantity=5 | | |
| TC-B-02 | Add item with quantity=1 (on point, min valid) | `{..., quantity:1}` | Logged in | POST /api/cart | 200; quantity=1 accepted | | |
| TC-B-03 | Add item with quantity=0 (off point, D-Q2) — **bug revelation** | `{..., quantity:0}` | Logged in | POST /api/cart | **Server has no validation: 200 accepted, item added with quantity=0** — this confirms a server-side input validation bug → **BUG-B-01** | | |
| TC-B-04 | Add item with negative quantity (D-Q3) — **bug revelation** | `{..., quantity:-1}` | Logged in | POST /api/cart | **Server has no validation: 200 accepted, item added with quantity=-1** — cart total becomes negative → **BUG-B-01** | | |
| TC-B-05 | Add item with non-integer quantity string (D-Q4, mobile) | Quantity input = `"abc"` in mobile UI | Logged in, on product detail | Tap "Add to cart" | Mobile normalizes to 1; item added with quantity=1 | | |
| TC-B-06 | Add item with float quantity (D-Q5, mobile) | Quantity input = `"1.5"` | Logged in | Tap "Add to cart" | Mobile: `parseInt("1.5")=1`, item added with quantity=1 | | |
| TC-B-07 | Checkout with valid total_amount (D-T1) | `{total_amount:200000, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | 200, order created with `status=pending` | | |
| TC-B-08 | Checkout with total_amount=0 (off point, D-T2) — **bug revelation** | `{total_amount:0, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | **Server does not validate total_amount: 200 accepted, order created with total=0** → **BUG-B-02** | | |
| TC-B-09 | Checkout with negative total_amount (D-T3) — **bug revelation** | `{total_amount:-1, shipping_address:"123 Le Loi"}` | Cart has items | POST /api/checkout | **Server does not validate total_amount: 200 accepted, order created with total=-1** → **BUG-B-02** | | |
| TC-B-10 | Checkout with empty shipping_address (D-A2) | `{total_amount:200000, shipping_address:""}` | Cart has items | POST /api/checkout | Should reject (400) — address is a required field; empty string is not a valid delivery address | | |
| TC-B-11 | Checkout with arbitrary total_amount — price manipulation bypass | `{total_amount:1, shipping_address:"addr"}` | Cart has items worth 500,000 | POST /api/checkout directly (API) | **Server accepts any value — no cart-total verification** → **BUG-B-02** | | |
| TC-B-12 | Add same product twice — duplicate entry behaviour | Add product id=1 twice with qty=3 each | Cart empty | 2× POST /api/cart | **Server uses push() — cart array contains TWO separate entries for id=1 (each with qty=3), not one merged entry with qty=6** → **BUG-B-04** | | |
| TC-B-13 | GET cart when empty | No body | Logged in, cart has no items | GET /api/cart | 200 with empty array `[]`; no error | | |
| TC-B-14 | Add item to cart without authentication (D-Auth2) | `{id:1, name:"X", price:100000, quantity:1}` | Not logged in / no token | POST /api/cart | 401 Unauthorized — cart requires authentication | | |
| TC-B-15 | Checkout without authentication (D-Auth2) | `{total_amount:200000, shipping_address:"123 Le Loi"}` | Not logged in / no token | POST /api/checkout | 401 Unauthorized — checkout requires authentication | | |
| TC-B-16 | Checkout with empty cart | `{total_amount:0, shipping_address:"123 Le Loi"}` | Logged in, cart is empty | POST /api/checkout | Should reject (400) — cannot create order from empty cart | | |
| TC-B-17 | Checkout with null shipping_address (D-A3) | `{total_amount:200000, shipping_address:null}` | Cart has items | POST /api/checkout | Should reject (400) — null address must be rejected | | |
| TC-B-18 | Add item with manipulated price = 0 (D-PR2) — **security** | `{id:1, name:"X", price:0, quantity:1}` | Logged in | POST /api/cart | **Server accepts price=0; cart total computed as 0×1=0; item acquired for free** → **BUG-B-05** | | |
| TC-B-19 | Add item with negative price (D-PR3) — **security** | `{id:1, name:"X", price:-50000, quantity:1}` | Logged in | POST /api/cart | **Server accepts negative price; cart total goes negative** → **BUG-B-05** | | |
| TC-B-20 | Cart total calculation accuracy | Add item `{price:150000, quantity:3}` and item `{price:75000, quantity:2}` | Logged in, cart empty | 2× POST /api/cart, then GET /api/cart | Cart total = `(150000×3) + (75000×2) = 600000`; verify `cart.reduce()` is correct | | |
| TC-B-21 | Add item with extremely large quantity (D-Q7, upper edge) | `{..., quantity:2147483647}` | Logged in | POST /api/cart | Server should reject or cap; if accepted, cart total may overflow → edge behaviour documented | | |
| TC-B-22 | XSS injection in shipping_address (D-A5) — **security** | `{total_amount:200000, shipping_address:"<script>alert(1)</script>"}` | Cart has items | POST /api/checkout | 200 or 400; no script executes; input safely stored/escaped | | |

#### Constraint-based Test Cases (OWASP / Security)

> These test cases cover security constraints derived from OWASP Top 10 and general API security best practices.

| TC ID | Constraint | Objective | Input | Pre-condition | Steps | Expected (best practice) | Actual Result | Verdict |
|-------|-----------|-----------|-------|---------------|-------|--------------------------|---------------|---------|
| TC-B-C-01 | OWASP A04 (Insecure Design) | Price manipulation via crafted POST body | `{id:1, name:"Laptop", price:1, quantity:1}` | Logged in; actual product price = 15,000,000 | POST /api/cart with price=1; then POST /api/checkout with total_amount=1 | **Best practice:** server should source `price` from the product database, not the request body. Order should be rejected or corrected. **Current:** server accepts price=1 from client → **BUG-B-05** | | |
| TC-B-C-02 | OWASP A04 (Insecure Design) | Total amount bypass at checkout | Cart with items totalling 500,000; POST checkout with `total_amount:1` | Logged in; cart has items | POST /api/checkout directly with manipulated `total_amount` | **Best practice:** server should compute total from cart contents and reject mismatched `total_amount`. **Current:** any value accepted → **BUG-B-02** | | |
| TC-B-C-03 | OWASP A07 (Auth Failures) | Cart access without valid session | No auth token | N/A | GET /api/cart with no token | **Best practice:** 401 Unauthorized | | |
| TC-B-C-04 | OWASP A03 (Injection) | XSS attempt in product name stored via cart | `{id:1, name:"<img src=x onerror=alert(1)>", price:100, quantity:1}` | Logged in | POST /api/cart, then GET /api/cart; render cart in UI | **Best practice:** no script/alert executes; name safely escaped in rendering | | |

### 3.2 Boundary Value Analysis

#### Step-by-step Technique Application

**Step 1 — Identify variables with testable boundaries**

BVA applies to variables whose valid/invalid partition has an ordered, measurable boundary. Four variables qualify:

| Variable | Observable Range | Key Boundary |
|----------|-----------------|--------------|
| `quantity` (mobile `normalizeQuantity`) | Any integer → normalised | `parsed > 0` threshold; `parseInt()` truncation of floats |
| `quantity` (server-side, no upper cap) | 1 → ∞ (server accepts all) | Minimum valid (1); extreme large values causing total overflow |
| `total_amount` at checkout | Any integer (no server check) | `> 0` is the expected valid threshold; 0 and negatives are edge cases |
| `shipping_address` length | 0 chars → ∞ | Empty (0 chars) vs non-empty (1 char); extremely long strings |

---

**Step 2 — Determine boundary points**

**Variable 1: `quantity` — mobile `normalizeQuantity()` (`parseInt(value) > 0 ? parsed : 1`)**

| BVA Point | Value | Expected normalised result |
|-----------|-------|---------------------------|
| Out point (negative) | `-1` | `parseInt("-1") = -1`, not > 0 → normalised to `1` |
| Off point (just below threshold) | `0` | `parseInt("0") = 0`, not > 0 → normalised to `1` |
| On point (threshold) | `1` | `parseInt("1") = 1`, > 0 → accepted as `1` |
| In point (typical valid) | `5` | accepted as `5` |
| Float truncation | `1.5` | `parseInt("1.5") = 1` → normalised to `1` |
| Float below 1 | `0.9` | `parseInt("0.9") = 0`, not > 0 → normalised to `1` |

**Variable 2: `quantity` — server-side (no upper cap)**

| BVA Point | Value | Description |
|-----------|-------|-------------|
| Off point (below min) | `0` | Invalid; server accepts (no validation) |
| On point (min valid) | `1` | Minimum meaningful quantity |
| In point | `5` | Normal use |
| Upper extreme | `999999` | No server cap — accepted; cart total may become very large |
| Integer overflow edge | `2147483647` | INT_MAX — server/JS number handling edge |

**Variable 3: `total_amount` at checkout**

| BVA Point | Value | Expected |
|-----------|-------|----------|
| Out point (negative) | `-1` | Invalid; server should reject → but currently **accepts** (bug) |
| Off point (zero — just below valid) | `0` | Invalid; server should reject → but currently **accepts** (bug) |
| On point (minimum valid) | `1` | Smallest valid order amount |
| In point (typical) | `200000` | Normal checkout amount |

**Variable 4: `shipping_address` length**

| BVA Point | Length | Value |
|-----------|--------|-------|
| Off point | 0 chars | `""` (empty — invalid) |
| On point | 1 char | `"A"` (minimal valid — debatable) |
| In point | Typical | `"123 Le Loi, Q1, TP.HCM"` |
| Upper edge | > 500 chars | 501-char string — no length cap defined |

---

**Step 3 — Design BVA test cases**

#### BVA Test Cases

| TC ID | Variable | BVA Point | Input | Pre-condition | Steps | Expected Result | Actual Result | Verdict |
|-------|----------|-----------|-------|---------------|-------|-----------------|---------------|---------|
| TC-B-BV-01 | quantity (mobile) | Out point — negative input | Quantity input = `-1` in mobile UI | Logged in | Enter `-1`, tap "Add to cart" | `normalizeQuantity`: `-1` not > 0 → item added with `quantity=1` | | |
| TC-B-BV-02 | quantity (mobile) | Off point — zero input | Quantity input = `0` in mobile UI | Logged in | Enter `0`, tap "Add to cart" | `normalizeQuantity`: `0` not > 0 → item added with `quantity=1` | | |
| TC-B-BV-03 | quantity (mobile) | On point — minimum valid | Quantity input = `1` in mobile UI | Logged in | Enter `1`, tap "Add to cart" | `parseInt("1")=1 > 0` → item added with `quantity=1` (accepted as-is) | | |
| TC-B-BV-04 | quantity (mobile) | Float truncation — `1.5` | Quantity input = `"1.5"` in mobile UI | Logged in | Enter `1.5`, tap "Add to cart" | `parseInt("1.5")=1 > 0` → item added with `quantity=1` | | |
| TC-B-BV-05 | quantity (mobile) | Float truncation — `0.9` (below 1) | Quantity input = `"0.9"` in mobile UI | Logged in | Enter `0.9`, tap "Add to cart" | `parseInt("0.9")=0`, not > 0 → normalised to `quantity=1` | | |
| TC-B-BV-06 | quantity (server) | On point — minimum valid (API) | `{..., quantity:1}` | Logged in | POST /api/cart | 200; item accepted with `quantity=1` | | |
| TC-B-BV-07 | quantity (server) | Off point — zero (API) | `{..., quantity:0}` | Logged in | POST /api/cart | **No server validation: 200 accepted with quantity=0** — confirms BUG-B-01 | | |
| TC-B-BV-08 | quantity (server) | Upper extreme — 999,999 | `{..., quantity:999999}` | Logged in | POST /api/cart | Server accepts; cart total = `price × 999999` — no overflow protection | | |
| TC-B-BV-09 | total_amount | On point — minimum valid (1) | `{total_amount:1, shipping_address:"addr"}` | Cart has items | POST /api/checkout | 200; order created (debatable: should this be valid? — but server accepts) | | |
| TC-B-BV-10 | total_amount | Off point — zero | `{total_amount:0, shipping_address:"addr"}` | Cart has items | POST /api/checkout | **No server validation: 200 accepted with total=0** — confirms BUG-B-02 | | |
| TC-B-BV-11 | total_amount | Out point — negative | `{total_amount:-100, shipping_address:"addr"}` | Cart has items | POST /api/checkout | **No server validation: 200 accepted with total=-100** — confirms BUG-B-02 | | |
| TC-B-BV-12 | shipping_address | Off point — empty string (0 chars) | `{total_amount:200000, shipping_address:""}` | Cart has items | POST /api/checkout | Should reject (400) — empty address not deliverable | | |
| TC-B-BV-13 | shipping_address | On point — 1 char | `{total_amount:200000, shipping_address:"A"}` | Cart has items | POST /api/checkout | Minimal acceptance; single character is functionally invalid but tests the boundary | | |
| TC-B-BV-14 | shipping_address | In point — typical | `{total_amount:200000, shipping_address:"123 Le Loi, Q1, TP.HCM"}` | Cart has items | POST /api/checkout | 200; order created successfully | | |
| TC-B-BV-15 | shipping_address | Upper edge — 501 chars | `{total_amount:200000, shipping_address:"A"×501}` | Cart has items | POST /api/checkout | No defined server cap — likely accepted; length limit should be documented | | |

### 3.3 AI Gap Analysis

**Bugs and gaps the AI initially missed or under-specified:**

1. **`price` as an attacker-controlled input (TC-B-18, TC-B-19, TC-B-C-01)** — The original domain analysis listed `price` as "taken from product data", implying it was a trusted value. In reality, since `POST /api/cart` pushes any body object directly, `price` is fully user-controllable. The AI did not flag this as a security-sensitive input variable. A malicious client can supply `price:1` for any product, reducing the cart total to negligible amounts.

2. **`total_amount` bypass at checkout (TC-B-11, TC-B-C-02)** — TC-B-11 was present but framed as a curiosity ("server accepts any value"). The AI did not escalate this as a critical security defect. The checkout endpoint performs no server-side reconciliation between the submitted `total_amount` and the computed cart total — this allows a client to check out a full cart for `total_amount:1`, constituting a price manipulation vulnerability.

3. **Authentication enforcement on cart/checkout endpoints (TC-B-14, TC-B-15, TC-B-C-03)** — The original test suite contained no test cases for unauthenticated access to `GET /api/cart`, `POST /api/cart`, or `POST /api/checkout`. Whether these endpoints properly reject unauthenticated requests is untested — a fundamental access-control gap.

4. **Duplicate product entries not merged (TC-B-12 correction)** — The original expected result for TC-B-12 stated "Cart shows product id=1 with quantity=6", implying the server merges duplicate entries. The actual code (`push()` to array) creates two separate entries. The AI generated an incorrect expected result by assuming cart-merge behaviour that does not exist in the implementation.

5. **Empty cart checkout (TC-B-16)** — The original test suite had no test for submitting a checkout request when the cart is empty. This is a basic functional boundary (can an order with zero items be created?) that was entirely omitted.

6. **Cart persistence boundary (BUG-B-03)** — The AI identified in Step 1 that the cart is stored in-memory (`userCarts` object). However, no test case was written to validate or document this behaviour. The implication — that all cart data is lost on server restart — is a reliability defect that should be explicitly tested and reported.

7. **XSS injection surface in cart data (TC-B-22, TC-B-C-04)** — Neither the product name field in the cart body nor the `shipping_address` field were tested for XSS payloads. The AI's initial analysis focused only on numeric validation and did not treat string fields as injection targets.

8. **`shipping_address` length boundary** — The original BVA table only identified boundaries for `quantity` and `total_amount`. No length boundary was considered for `shipping_address`, despite it being a free-form text field with no defined maximum length.

**Why the AI missed these:**
- It analysed the source code for validation logic and stopped at confirming "no validation exists" — without then deriving the *security impact* of that absence (price manipulation, auth bypass testing).
- It assumed standard e-commerce behaviour (cart quantity merging, server-side price sourcing) rather than testing the actual implementation's behaviour.
- It did not apply OWASP's Insecure Design (A04) lens to the API design, which would have immediately flagged that `price` must never be client-supplied.

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
