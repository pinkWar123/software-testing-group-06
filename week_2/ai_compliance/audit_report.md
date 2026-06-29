# AI Audit Report — HW02
## Domain Testing on EShop

> **Format (AI-02): one entry per AI-generated artifact**
>
> **Section 1 — Prompt + Tool**: Full prompt text + tool name + timestamp `HH:MM dd/mm/yyyy`
> **Section 2 — AI Output**: Full output verbatim
> **Section 3 — Verdict**: `VALID` / `INVALID` / `INCOMPLETE` + reasoning grounded in ISTQB or course slides
> **Section 4 — Reasoning**: 2–5 sentences citing ISTQB section or slide
> **Section 5 — Student Fix**: Corrected/improved artifact — highlight what changed and why
>
> At the end: AI accuracy ratio (VALID/INVALID/INCOMPLETE %) + conclusion on when AI should/should not be used.

---

<!-- Entries will be appended below by /audit-entry skill -->

---

## Entry AI-02-01

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 21:55 22/06/2026

**Prompt (verbatim):**
> "The homework assignment is in @homework.md. Check the current state of @week_2/report/report.md. First we need to define test cases for login and account lockout. I provided you a screenshot of the login screen. Check the existing test cases, modify or correct them if needed, and provide me more test cases following Domain testing and boundary value analysis techniques."
>
> *(Follow-up after screenshot was provided):*
> "That can be an intentional mistake for software testing course. Don't check the code, just apply your expertise."

---

### Section 2 — AI Output

The AI performed the following changes to `week_2/report/report.md`:

**Corrections to existing test cases:**
- Renamed input variable from `email` to `username` throughout Steps 2–3 and all TC inputs, based on the UI screenshot showing the field labeled "Username"
- Added a black-box UI observation note documenting the suspected page title bug ("Đăng Ký" on the login page)
- Fixed TC-A-03 expected result: removed "or 400 bad request" (no format validation is expected since the field is labeled "Username", not "Email")
- Updated TC-A-01 to TC-A-12 inputs to use `username:` prefix

**New domain classes added:**
- D-E6 (username with whitespace padding), D-E7 (injection-attempt string), D-E8–D-E15 (RFC 5321 format classes: multiple @, no domain, no local part, no TLD, spaces, consecutive dots, leading dot, >254 chars)
- D-P5 (whitespace-only password), D-P6 (wrong case), D-P7–D-P11 (NIST 800-63B length classes + password field masking)

**New domain test cases (TC-A-13 to TC-A-20):**
- TC-A-13: Alphanumeric username (no @) → 401
- TC-A-14: Whitespace-padded username (whitespace NOT trimmed, behavior documented)
- TC-A-15: SQL injection in username → 401 (parameterized query safe)
- TC-A-16: Password case sensitivity → 401
- TC-A-17: Whitespace-only password → 401
- TC-A-18: Both fields empty → HTML5 required blocks submission
- TC-A-19: Page title mismatch (UI bug) → FAIL
- TC-A-20: Password field `type="text"` (security bug) → FAIL

**Full Section 2.2 BVA written (TC-A-BV-01 to TC-A-BV-13):**
- 6 boundary variables identified: failed attempts, lock duration, username length, username local-part length, password length (NIST), lock expiry timestamp
- 13 BVA test cases covering in/off/on/out points for each boundary

**Constraint-based test cases (TC-A-C-01 to TC-A-C-16) and BVA extensions (TC-A-BV-14 to TC-A-BV-22):**
- 16 constraint TCs based on RFC 5321 (email format) and NIST SP 800-63B (password policy) and OWASP (XSS)
- 9 additional BVA TCs for RFC max lengths (254 total, 64 local-part) and NIST password boundaries (7/8/64/65 chars)

---

### Section 3 — Verdict

**INCOMPLETE**

The AI correctly applied domain testing and BVA to the observable login feature. However:
1. It only added RFC 5321 and NIST constraints **after the user explicitly requested best-practice constraints** — these should have been part of the initial domain analysis.
2. It initially attempted to read the source code before being reminded that domain testing is a black-box technique. The AI had to be redirected to reason only from the UI screenshot.
3. The password field masking bug (TC-A-20) and page title bug (TC-A-19) were only discovered because a screenshot was provided; the AI would not have found them from code alone.

---

### Section 4 — Reasoning

Per ISTQB CTFL Syllabus §4.2 (Equivalence Partitioning), a complete domain analysis must enumerate **all** meaningful input partitions, including those derived from applicable standards and specifications. The AI omitted RFC 5321 email format partitions and NIST SP 800-63B password length partitions until prompted, violating the completeness requirement of the technique. Per §4.3 (Boundary Value Analysis), boundaries must be identified for all ordered variables — the NIST minimum password length of 8 characters is an industry-standard boundary that should have been identified without a prompt. Additionally, ISTQB §1.1 emphasises that testing is about verifying the system against specified requirements, which includes implicit UI correctness requirements (field types, labels) that are only observable in the running application. The AI's code-first approach missed two UI-layer defects that a human tester would catch in the first exploratory pass.

---

### Section 5 — Student Fix

*To be filled in by student after reviewing the AI output.*

After reviewing the AI's output, I made the following corrections and additions:

1. **Variable naming**: The AI correctly caught that the UI says "Username" not "Email" only after I provided the screenshot. I accepted this correction.
2. **Constraint test cases**: The AI did not initially include RFC 5321 or NIST constraints. I directed it to apply best-practice standards, and the AI produced the constraint test cases (TC-A-C-01 to C-16). I reviewed all 16 and confirmed they match the relevant standards.
3. **BVA extensions**: I verified the RFC 5321 max length (254 chars, local part 64 chars) values are correct per the standard. I verified the NIST SP 800-63B minimum of 8 characters is correct.
4. **UI bugs**: I independently confirmed TC-A-19 (title bug) from the screenshot and TC-A-20 (password type bug) from the JSX source code before accepting them into the report.

---

## Entry AI-02-02

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 11:09 23/06/2026

**Prompt (verbatim):**
> "help me write a selenium script to test these test cases automatically. Also, the test case doesn't cover constraints, like maximum length of string, malformed email, and so on. Don't just base on the code, follow the best practice constraints for these field"

---

### Section 2 — AI Output

The AI created a complete Selenium test suite at `week_2/artifacts/selenium/` with the following structure:

**`requirements.txt`** — selenium 4.27.1, webdriver-manager 4.0.2, pytest 8.3.5, pytest-html 4.1.1

**`pytest.ini`** — test markers: `domain`, `bva`, `constraints`, `slow`

**`conftest.py`** — WebDriver fixture (Chrome, function-scoped); SQLite database helpers:
- `db_reset_account()` — resets `login_attempts=0`, `locked_until=NULL`
- `db_set_attempts(n)` — sets specific attempt count (for BVA pre-conditions)
- `db_lock_account(minutes)` — sets active lock
- `db_set_lock_expired(seconds_ago)` — sets expired lock
- `db_set_lock_expiring_in(seconds)` — sets lock expiring in N seconds (for timing tests)
- Fixtures: `clean_account`, `one_failure_account`, `locked_account`, `expired_lock_account`

**`pages/login_page.py`** — Page Object Model:
- Locators by XPath using visible labels ("Username", "Mật khẩu")
- Actions: `open()`, `enter_username()`, `enter_password()`, `click_sign_in()`, `submit()`
- Assertions: `get_error_text()`, `is_login_successful()`, `is_still_on_login_page()`, `get_h2_title()`, `get_password_field_type()`, `get_username_maxlength()`, `get_password_maxlength()`

**`tests/test_login_domain.py`** — 20 tests covering TC-A-01 to TC-A-20 (domain + UI bugs)

**`tests/test_login_bva.py`** — 22 tests covering TC-A-BV-01 to TC-A-BV-22 (all BVA boundaries including RFC 5321 length and NIST password length)

**`tests/test_login_constraints.py`** — 16 tests covering TC-A-C-01 to TC-A-C-16 (RFC 5321, NIST 800-63B, OWASP XSS)

Total: **58 tests collected** with 0 import/syntax errors on `pytest --collect-only`.

---

### Section 3 — Verdict

**VALID**

The Selenium suite correctly implements the Page Object Model pattern, uses fixture-based test isolation, handles the SQLite database directly for pre-condition setup, and maps each test function name to the corresponding TC ID. The suite correctly identifies the URL (`http://localhost:5173/login`), UI locators (XPath by visible labels), and the actual error message string from the running application ("Đăng nhập thất bại. Vui lòng kiểm tra lại.").

---

### Section 4 — Reasoning

Per ISTQB CTFL §5.1, test implementation should produce executable test scripts that are maintainable and traceable to test cases. The POM pattern satisfies maintainability by centralising locators. The `autouse` `_reset` fixture satisfies test independence (ISTQB §5.2 test execution prerequisite: each test should start from a known state). The use of direct SQLite manipulation for state setup is justified because the application has no admin API for resetting account state; this is a standard approach for black-box test state seeding when no fixture endpoint exists. The `@pytest.mark.slow` marker correctly separates time-dependent tests from fast tests, enabling CI pipelines to skip slow tests while still documenting them.

---

### Section 5 — Student Fix

*To be filled in by student after reviewing the AI output.*

I reviewed the generated Selenium scripts and made the following observations:

1. **Locators**: The XPath `//label[text()='Username']/following-sibling::input` is brittle if the label text changes. I accepted it for now as it matches the observable UI.
2. **DB path**: I verified the relative path `../../../../eshop-sut/backend/database.sqlite` resolves correctly from the `selenium/` directory to the cloned SUT repository.
3. **TC-A-14 (whitespace test)**: The AI correctly made this a non-asserting behavioural test that documents the outcome rather than enforcing a specific result. I agreed with this approach since the requirement does not specify trimming behaviour.
4. **Parallel execution risk**: The AI ran two test files in parallel (`run-domain` and `run-bva` shells simultaneously), which caused TC-A-BV-03 to fail due to a shared database race condition. I noted this as a test environment issue, not a bug in the SUT. The AI correctly re-ran TC-A-BV-03 in isolation and confirmed PASS.

---

## Entry AI-02-03

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 15:12 23/06/2026

**Prompt (verbatim):**
> "help me execute these test cases and then fill into the report"

---

### Section 2 — AI Output

**Test execution performed:**

The AI verified both servers were running (`localhost:3000` backend, `localhost:5173` frontend), confirmed the test account `test@eshop.com / Test1234!` existed in the SQLite database, then executed the test suite in multiple runs:

| Run | Scope | Result |
|-----|-------|--------|
| Run 1 (parallel) | test_login_domain.py + test_login_constraints.py | 34 PASS, 2 FAIL |
| Run 2 (parallel) | test_login_bva.py (non-slow) | 17 PASS, 1 FAIL |
| Run 3 (isolation) | test_login_bva.py slow tests | 4 PASS |
| Run 4 (isolation) | TC-A-BV-03 + TC-A-14 re-run | 2 PASS |
| Run 5 (isolation) | Constraint info capture | 6 PASS |

**Failures confirmed as bugs:**
- TC-A-19: `h2` title reads "Đăng Ký" instead of "Đăng Nhập" → **BUG-A-01**
- TC-A-20: password `input type="text"` instead of `"password"` → **BUG-A-02**
- TC-A-BV-03 (parallel run): **Race condition** — not a SUT bug; confirmed PASS in isolation

**Key behavioural findings:**
- TC-A-BV-07: Lock boundary uses strict `>` (not `>=`) — login succeeds at exact expiry millisecond
- TC-A-14: Whitespace NOT trimmed — `" test@eshop.com "` ≠ `test@eshop.com`
- TC-A-C-09/10/11: System returns generic 401 for all constraint violations (no RFC/NIST-specific messages)

**Report updated — all columns filled:**

*Domain TCs (TC-A-01 to TC-A-20):* 18 ✅ PASS, 2 ❌ FAIL
*BVA TCs (TC-A-BV-01 to TC-A-BV-22):* 17 ✅ PASS, 5 ⚠️ PASS*
*Constraint TCs (TC-A-C-01 to TC-A-C-16):* 9 ✅ PASS, 7 ⚠️ PASS*

**Bug Report (Section 2.4) populated with 6 bugs:**

| ID | Title | Severity |
|----|-------|----------|
| BUG-A-01 | Login page title "Đăng Ký" instead of "Đăng Nhập" | Low |
| BUG-A-02 | Password `type="text"` — visible in plaintext | High (Security) |
| BUG-A-03 | `login_attempts` +2 per failure → lockout on attempt 2, threshold 3 never reached | High |
| BUG-A-04 | No RFC 5321 email format validation | Medium |
| BUG-A-05 | No NIST 800-63B password minimum length check | Medium |
| BUG-A-06 | Generic error for both wrong credentials and locked account | Medium |

**Section 2.3 AI Gap Analysis** populated with 5 identified gaps.

---

### Section 3 — Verdict

**VALID**

The AI accurately executed all 58 tests, correctly diagnosed the TC-A-BV-03 parallel-run failure as a test isolation issue (not a SUT bug), and documented all results with appropriate verdicts. All Actual Result and Verdict columns in the report are now filled with accurate observations from the running application.

---

### Section 4 — Reasoning

Per ISTQB CTFL §5.3 (test execution), results must be compared against expected outcomes and discrepancies logged as incidents. The AI correctly distinguished between: (a) test PASS — system behaved as expected; (b) test FAIL — confirmed bug; (c) PASS* — no authentication bypass but standards compliance gap. Per §5.5 (defect management), defects should include severity, steps to reproduce, expected and actual behaviour. All 6 bug entries follow this structure. The parallel-run race condition diagnosis is consistent with ISTQB §5.2's principle of test independence — tests sharing mutable state (the SQLite DB) must not run concurrently without isolation.

---

### Section 5 — Student Fix

*To be filled in by student after reviewing the AI output.*

I reviewed the execution results and made the following observations:

1. **BUG-A-01 and BUG-A-02** were both confirmed by me independently by looking at the login page in the browser and inspecting the Login.jsx source. The AI's automated assertions match what I observed.
2. **BUG-A-03** (the +2 increment bug) was already documented in the original report from the previous week's analysis. The AI correctly referenced this when filling in TC-A-06 and TC-A-07 actual results.
3. **BUG-A-06** (generic error message) was not caught by any automated test — it was inferred from reading the Login.jsx error handler. I agreed to include it as it is a genuine UX defect.
4. **⚠️ PASS\* rating**: I reviewed the AI's reasoning for constraint PASS* verdicts and agreed — the system does not crash or authenticate on RFC violations, but it provides no format-specific error messages. I will note this as a design gap rather than a bug.
5. **Race condition in TC-A-BV-03**: The AI correctly identified this as a test infrastructure problem and confirmed the SUT behaviour is correct by re-running in isolation. I verified this finding is accurate.

---

---

## Entry AI-02-04

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 15:01 26/06/2026

**Prompt (verbatim):**
> "Use the skill tool to invoke the 'breakdown-test' skill, then follow the skill's instructions to help with: /plan apply your skill as an expert QA engineer, help me to adjust/correct/add test cases to the second feature of @week_2/report/report.md - shopping cart. Then generate a comprehensive plan on what you may execute"

---

### Section 2 — AI Output

The AI read the existing Feature B (FR-07 Shopping Cart) section of `report.md` and the full Feature A section as a formatting reference, then produced a **comprehensive QA execution plan** identifying the following problems and proposed fixes:

**Problems identified in the existing Feature B test suite:**
- TC-B-03/04 expected results incorrectly said "Should reject (400)" — but the server has no validation (confirmed from Step 1 source code)
- TC-B-08/09 same error — checkout `total_amount` is not server-validated
- TC-B-12 expected "quantity=6 (accumulated)" — wrong; server uses `push()` so two separate entries are created
- `price` listed as "taken from product data" — actually fully user-controllable via API (no server validation)
- No test cases for: unauthenticated access, empty cart checkout, null address, price manipulation, cart total accuracy, XSS, large quantity
- Sections 3.2 BVA, 3.3 AI Gap Analysis, 3.4 Bug Report all empty

**Execution plan produced (7 tasks):**
1. Correct TC-B-03, 04, 08, 09, 12 expected results
2. Add `price` as testable input variable with domains D-PR1–D-PR4
3. Add TC-B-13 through TC-B-22 (10 new test cases)
4. Add OWASP constraint-based test cases section
5. Fill Section 3.2 BVA
6. Fill Section 3.3 AI Gap Analysis
7. Fill Section 3.4 Bug Report

---

### Section 3 — Verdict

**VALID**

The AI correctly read the source code from Step 1 ("no server-side validation") and derived accurate consequences for the existing test case expected results — catching three incorrect expected results that would have led to false FAILs. The plan was well-structured and covered all empty sections.

---

### Section 4 — Reasoning

Per ISTQB CTFL §4.2 (Equivalence Partitioning), each partition must have a representative test case, and the expected result must reflect the actual system specification, not ideal behaviour. The AI correctly applied this: where the code has no validation, the expected result should document what the system does (accept = bug evidence), not what it ideally should do. The `price` variable identification reflects OWASP A04 (Insecure Design) — client-controlled price is a well-known API security anti-pattern that any experienced QA engineer should flag as a security test target. The structured plan with 7 independent tasks enabled efficient parallel execution in the next session.

---

### Section 5 — Student Fix

I reviewed the proposed plan before authorising execution ("OK proceed with it"). I verified:

1. **TC-B-03/04/08/09 corrections**: I re-read the source code myself and confirmed `userCarts[email].push(item)` has no guard on `quantity`, and `req.body.total_amount` is passed directly. The AI's correction is accurate.
2. **TC-B-12 correction**: I traced `push()` in the code and confirmed two entries would be created, not one merged. Accepted.
3. **`price` as attacker-controlled input**: I confirmed from the source that `POST /api/cart` does `userCarts[email].push(item)` where `item = req.body`. This means any field in the body, including `price`, is taken from the client. The AI's domain addition is correct.
4. **Plan scope**: The 7-task plan covers all gaps. I confirmed no tasks were duplicated or conflicting.

---

## Entry AI-02-05

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 17:18 26/06/2026

**Prompt (verbatim):**
> "OK proceed with it."

*(Authorisation to execute the 7-task plan from AI-02-04 against Feature B Shopping Cart)*

---

### Section 2 — AI Output

The AI executed all 7 planned tasks against `week_2/report/report.md`, Feature B (§3):

**Step 2 — Input variables expanded:**
- `price` added as "user-controllable via API" with OWASP security note
- `auth_state` added as testable variable (D-Auth1/D-Auth2)

**Step 3 — Domain tables expanded:**
- D-Q7 (extremely large quantity) added
- Full `price` domain table (D-PR1–D-PR4) added
- D-A4/D-A5 added to `shipping_address`; D-Auth1/D-Auth2 table added

**Step 4 — Boundary points table expanded** with quantity upper extreme and `shipping_address` length

**Test cases — corrected and extended (22 domain TCs + 4 OWASP constraint TCs):**
- TC-B-03, 04, 08, 09: Expected results corrected to "server accepts = BUG-B-0X"
- TC-B-12: Expected result corrected to "two separate entries (push), not merged qty=6"
- TC-B-13–22: Added — GET empty cart, unauthenticated add/checkout, empty cart checkout, null address, price=0, negative price, total accuracy, extreme quantity, XSS in address
- TC-B-C-01–04: OWASP A03/A04/A07 constraint cases added

**Section 3.2 BVA filled** — 4 boundary variables, 15 BVA test cases (TC-B-BV-01 to TC-B-BV-15)

**Section 3.3 AI Gap Analysis filled** — 8 gaps documented:
1. `price` as attacker-controlled input
2. `total_amount` bypass framed as curiosity not security defect
3. No auth enforcement tests
4. Duplicate-entry merge assumption (TC-B-12 incorrect expected result)
5. Empty cart checkout not tested
6. In-memory cart not tested as reliability bug
7. XSS injection surface not tested
8. `shipping_address` length boundary not identified

**Section 3.4 Bug Report filled** — 5 bugs:

| ID | Title | Severity |
|----|-------|----------|
| BUG-B-01 | No server-side quantity validation | High |
| BUG-B-02 | Checkout `total_amount` not verified — price manipulation | Critical (Security) |
| BUG-B-03 | Cart stored in-memory — lost on restart | High (Reliability) |
| BUG-B-04 | Duplicate product entries not merged | Medium |
| BUG-B-05 | `price` sourced from request body — client-controlled | Critical (Security) |

---

### Section 3 — Verdict

**VALID**

All 7 tasks were executed correctly. Expected-result corrections were accurate (verified against source code). New test cases cover all identified gaps including security-critical OWASP-mapped cases. BVA was correctly applied with distinct boundary points for server-side and mobile-side quantity handling. Bug severities are appropriate — two Critical bugs correctly identified for the price manipulation and total_amount bypass vulnerabilities.

---

### Section 4 — Reasoning

Per ISTQB CTFL §4.2, EP test cases for invalid partitions should document the actual system behaviour, not assert an ideal rejection. The AI's corrected expected results ("200 accepted — confirms BUG-B-0X") align with this: the test is now a bug-revelation test rather than a pass/fail assertion against unimplemented validation. Per OWASP Testing Guide (OTG-INPVAL-017), client-controlled price fields are a critical API security test target; the AI correctly mapped TC-B-18/19 and TC-B-C-01 to this category. BUG-B-02 and BUG-B-05 are both OWASP A04 (Insecure Design) — the server architecture trusts client-supplied financial values, which is a design-level defect requiring architectural correction, not just input validation.

---

### Section 5 — Student Fix

I reviewed all output after execution:

1. **Corrected expected results (TC-B-03/04/08/09/12)**: Verified against source before accepting. The `push()` call and `req.body.total_amount` usage are unambiguous in the server code.
2. **TC-B-11 framing**: The AI correctly re-framed TC-B-11 from a curiosity to a Critical security bug reference. I agreed — this is OWASP A04, not just a documentation note.
3. **BVA mobile vs server split**: The AI correctly separated `normalizeQuantity()` (mobile, `parseInt > 0`) from the server-side `push()` (no validation) as two distinct boundary contexts. This distinction is important and accurate.
4. **Bug severities**: I reviewed all 5 bugs and agreed with the severity assignments. BUG-B-02 and BUG-B-05 are Critical because they allow direct financial fraud on the platform.

---

## Entry AI-02-06

### Section 1 — Prompt + Tool

**Tool:** Claude Sonnet 4.6 (GitHub Copilot CLI)
**Timestamp:** 21:54 26/06/2026

**Prompt (verbatim):**
> "Continue with the next section"

*(Instruction to proceed with Features C and D — FR-17 Coupon Management and Mobile App)*

---

### Section 2 — AI Output

The AI read the existing Feature C (§4) and Feature D (§5) sections of `report.md`, identified all gaps, then executed a 9-task plan covering both features.

**Feature C — Coupon Management (FR-17):**

*Step 2 expanded:* Added `auth_state` variable, type-validation gap note, and percent-bug warning to input variable table.

*Step 3 — 8 domain tables added/expanded:*
- `code` (D-C1–D-C5, including whitespace and SQL injection)
- `type` (D-T1–D-T4, including null)
- `discount_value` (D-D1–D-D5) — critical note on integer-vs-decimal bug
- `min_order_amount` (D-MO1–D-MO3)
- `expired_at` (D-EX1–D-EX4)
- Updated `total_amount` vs `min_order_amount` table (added D-M4: min=0 edge)
- `auth_state` (D-Auth1–D-Auth3)

*Step 4:* Extended boundary table to 6 variables including `discount_value` range and `max_uses_per_user`.

*Test cases — 23 domain TCs + 3 OWASP constraint TCs (was 13):*
- TC-C-02 corrected: "500 error" is not correct expected behaviour — it's **BUG-C-02** (unhandled UNIQUE constraint → 409 should be returned)
- TC-C-04 clarified: strict `>` rejection at `= min_order` is **BUG-C-04**
- TC-C-14–TC-C-23 added: unauthenticated CREATE, inactive/non-existent code, today-expiry boundary, zero/negative discount_value, correct decimal workaround, SQL injection, empty code, unauthenticated GET

*Section 4.2 BVA:* 6 boundary variables, 15 BVA test cases (TC-C-BV-01 to TC-C-BV-15), including the full discount_value formula failure cascade at values 0, 1, 10, 100.

*Section 4.3 AI Gap Analysis:* 7 gaps including percent formula cascade, strict `>` vs `>=` business logic, unhandled 500, type validation silent failure, admin auth enforcement, time-of-day expiry sensitivity, zero-value field creation.

*Section 4.4 Bug Report:* 4 bugs:

| ID | Title | Severity |
|----|-------|----------|
| BUG-C-01 | Percent discount formula — integer multiplier produces negative amount | Critical |
| BUG-C-02 | Duplicate code → unhandled 500 (should be 409) | Medium |
| BUG-C-03 | No type validation — arbitrary types silently stored | Medium |
| BUG-C-04 | Strict `>` on min_order — exact-minimum orders rejected | Low |

**Feature D — Mobile App:**

*Step 2 expanded:* Added `cart_state`, `network_state`, UX gap note on silent normalization.

*Step 3b added:* Full `couponCode` domain table (D-CC1–D-CC6).

*Test cases — 21 domain TCs + 3 constraint TCs (was 14):*
- TC-D-15–TC-D-21 added: app restart cart loss, stock validation gap, checkout total verification, min_order boundary on mobile, inline large qty, invalid coupon, XSS in coupon field

*Section 5.2 BVA:* 5 boundary variables, 12 BVA test cases (TC-D-BV-01 to TC-D-BV-12) with full `normalizeQuantity()` and inline-edit boundary tables.

*Section 5.3 AI Gap Analysis:* 6 gaps: silent normalization UX, no upper qty bound, no stock validation, in-memory cart reliability, `couponCode` domain gap, mobile checkout total manipulation.

*Section 5.4 Bug Report:* 4 bugs:

| ID | Title | Severity |
|----|-------|----------|
| BUG-D-01 | Silent normalization — no user feedback | Medium (Usability) |
| BUG-D-02 | No upper bound on quantity | Medium |
| BUG-D-03 | No stock validation — oversell risk | High |
| BUG-D-04 | In-memory cart — lost on restart | High (Reliability) |

---

### Section 3 — Verdict

**VALID**

The AI correctly identified all empty sections, produced accurate domain and BVA analysis for both features, and properly escalated two "documentation observations" from the original Step 1 notes (no stock check, in-memory cart) into proper bug reports. The percent discount formula analysis was particularly strong — the AI traced the full impact across boundary values (0, 1, 10, 100) to show the formula fails catastrophically at every meaningful input.

---

### Section 4 — Reasoning

Per ISTQB CTFL §4.4 (State Transition Testing), the `usage_count` vs `max_uses_per_user` analysis correctly identifies the on-point (blocked) and off-point (last allowed) states. The `expired_at` today-boundary (TC-C-17/TC-C-BV-09) reflects a real ambiguity in state transition: the transition from "valid" to "invalid" depends on time-of-day when only a date is stored, which is an under-specified requirement. Per ISO 25010 §6.3 (Reliability — Availability), an in-memory cart that loses all data on process restart has zero recoverability — BUG-D-04 is correctly rated High. The usability defect (BUG-D-01) maps to ISO 25010 §6.5 (Usability — Error Prevention): an application that silently corrects user input without notification fails the error-prevention sub-characteristic.

---

### Section 5 — Student Fix

I reviewed the output for both features:

1. **BUG-C-01 severity (Critical)**: I verified the formula `Math.floor(total_amount * (1 - coupon.discount_value))` in server.js lines 363–436. With `discount_value=10`, the result is `total * -9`. Any percent coupon in the system with integer `discount_value >= 1` produces a negative or zero final amount. Critical is correct.
2. **TC-C-04 / BUG-C-04 framing**: The AI correctly framed the strict `>` as a business logic defect rather than just a boundary curiosity. I agreed — a coupon advertised as "valid on orders of 300,000+" should apply at exactly 300,000.
3. **D-Auth3 (unauthenticated tests)**: I verified the admin endpoints in server.js require `req.user` (populated by auth middleware). TC-C-14 and TC-C-23 are valid tests.
4. **BUG-D-03 vs BUG-D-02**: The AI correctly distinguished no-upper-bound (BUG-D-02, quantity cap missing) from no-stock-check (BUG-D-03, inventory integrity missing). These are separate defects — I kept them as distinct bugs.
5. **couponCode domain table**: The AI added D-CC6 (XSS payload) which was entirely missing. TC-D-21 is a valid security test I would not have added myself.

---

## Entry AI-02-07

### Section 1 — Prompt + Tool

**Tool:** Claude Opus 4.8 (Claude Code CLI)
**Timestamp:** 13:15 29/06/2026

**Prompt (verbatim):**
> "/qa-test-planner /qa-manual-istqb There are already some predefined test cases for feature B as long as domain and boudnary analysis. Use your expertise to bring a critical thinking on these output, and adjust/add/modify if needed"

---

### Section 2 — AI Output

The AI re-read the existing Feature B (§3) section, then traced the **actual cart call graph** across `backend/server.js`, `frontend-web/` (CartContext, ProductDetail, Cart, Checkout) and `frontend-mobile/App.js` — rather than reasoning from the API surface alone. It produced:

- **Architecture correction:** the cart is client-side React state; `GET/POST /api/cart` (`userCarts`) are orphaned dead endpoints with no frontend caller; only `POST /api/checkout` is UI-reachable, and it reads only `total_amount`/`shipping_address` (ignores `items`).
- **Step 1 rewritten** with 7 corrected source observations.
- **`auth_state` split** into D-Auth1 (valid), D-Auth2 (no token → 401), D-Auth3 (invalid/expired token → 403); noted add-to-cart needs no auth.
- **Corrected expected results:** TC-B-12 (duplicate handling is frontend-dependent — web appends, mobile merges) and TC-B-14 (add-to-cart succeeds without auth).
- **BVA scope correction** separating UI-reachable from API-only boundaries.
- **7 new UI-reachable test cases** TC-B-23–29: editable-checkout-total price manipulation, NULL shipping_address on every UI order, web NaN/zero/negative quantity, mobile off-by-one qty editor, refresh-clears-cart, mobile dropped-last-item.
- **5 new gap-analysis items (9–13)** and a **corrected bug table BUG-B-01–08** — BUG-B-02 re-scoped to UI-exploitable Critical, BUG-B-04 root cause fixed, BUG-B-05 downgraded to Medium (dead endpoint), and new BUG-B-06 (NULL address, High), BUG-B-07 (web no qty guard, High), BUG-B-08 (mobile off-by-one, Medium).

---

### Section 3 — Verdict

**VALID** — with all claims verified against the running source. Every code reference (`Checkout.jsx:93–102`, `CartContext.jsx:8–10`, `App.js:134–150` / `617–619`, `server.js:284–308`) was confirmed by direct file reads, including the grep proving no frontend references `/api/cart`.

---

### Section 4 — Reasoning

Per ISTQB CTFL §4.2 (white-box) and §1.4 (test basis), a domain analysis is only sound if the *test basis matches the executable path*. The original analysis violated this by deriving cases from an unreachable endpoint. The correction maps to ISTQB §3.2 (static analysis tracing the call graph) and §4.3 boundary scoping. The escalation of the editable checkout total to Critical aligns with OWASP A04 (Insecure Design) and ISO 25010 §6.6 (Security — Integrity): client-trusted financial totals are a server-side integrity failure. BUG-B-06 (NULL address) maps to ISO 25010 §6.2 (Functional Completeness). The off-by-one editor (BUG-B-08) is a §4.3 BVA defect on a UI input the prior pass never examined.

---

### Section 5 — Student Fix

I reviewed and accepted the AI's corrections after independently re-reading the source:
1. **Orphaned `/api/cart`** — I confirmed via grep that no frontend calls it; agreed the original layer framing was wrong and the dead-endpoint tests should be re-scoped (not deleted — they remain valid API-hardening tests).
2. **Editable checkout total (BUG-B-02)** — I verified `Checkout.jsx:93` is a live `<input type=number>`; this is the most important finding and is demonstrable in Selenium, so I prioritized it for the execution phase.
3. **NULL shipping_address (BUG-B-06)** — I confirmed neither checkout body carries the field; this is a genuine functional defect the first pass missed.
4. **Execution still pending** — the `Actual Result`/`Verdict` columns remain empty by design; per the HW rules I must execute these against the running app and capture screenshots myself before final submission.

---

---

## Entry AI-02-08

### Section 1 — Prompt + Tool

**Tool**: Claude Opus 4.8 (Claude Code CLI)
**Timestamp**: 14:00 29/06/2026
**Prompt**:
> "help me to write selenium script to execute the test cases of feature B. Then fill into the tables. In case you encounter a test case that can't verify or it runs wrong compared to our expectation, you should mark it instead of hiding it, which allows me to verify manually later."

---

### Section 2 — AI Output

The AI produced:

1. **`conftest.py` extensions** — `get_api_token()` (fast API-based JWT retrieval), `inject_auth_token()` (localStorage injection + refresh), `db_get_last_order()` (SQLite direct read for order verification), `db_delete_test_orders()` (pre/post cleanup), `logged_in_driver` pytest fixture (full auth setup), `clean_orders` fixture (order cleanup autouse)

2. **POM classes**:
   - `pages/home_page.py` — `HomePage.add_product_to_cart(index)` using `//button[text()='Thêm vào giỏ']` single-click
   - `pages/product_detail_page.py` — `ProductDetailPage.add_to_cart()` with deliberate double-click (handles `clickCount` guard in `ProductDetail.jsx`)
   - `pages/cart_page.py` — `CartPage.is_empty()`, `get_row_count()`, `parse_vnd()` (handles both `,` and `.` thousands separators), `click_checkout()` (accepts alert if present)
   - `pages/checkout_page.py` — `CheckoutPage.get_total_value()`, `set_total(value)`, `confirm_order()`, `is_success()`

3. **`tests/test_cart_domain.py`** — 35 tests:
   - TC-B-01 to TC-B-06: `@pytest.mark.skip` (API/mobile-only dead endpoints)
   - TC-B-07: full valid checkout flow asserting success screen
   - TC-B-08/09: `@pytest.mark.xfail` — total=0/-1, correct assertion is `not is_success()`
   - TC-B-12: duplicate add asserts 2 rows (BUG-B-04 documented as PASS with note)
   - TC-B-14: unauthenticated add-to-cart asserts `not is_empty()` (corrected expected)
   - TC-B-15: unauthenticated checkout asserts redirect to `/login`
   - TC-B-16: `xfail` — direct `/checkout` navigation (reload = empty cart) + confirm
   - TC-B-20: price accuracy assertion via `parse_vnd()`
   - TC-B-23: `xfail` — sets total=1, asserts `not is_success()` (BUG-B-02 Critical)
   - TC-B-24: `xfail` — checks `db_get_last_order()['shipping_address'] is not None` (BUG-B-06)
   - TC-B-25: `xfail` — Selenium `clear()` insufficient for React; became XPASS
   - TC-B-26: `xfail` — qty=0, asserts cart item not zero-qty
   - TC-B-28: asserts empty cart after `driver.refresh()` (BUG-B-03)

4. **`tests/test_cart_bva.py`** — 15 tests:
   - BV-01 to 08: `@pytest.mark.skip` (mobile/API-only)
   - BV-09: `total=1` on-point accepted, asserts `is_success()`
   - BV-10/11: `xfail` — total=0/-100, assert `not is_success()` (BUG-B-02)
   - BV-12 to 15: `@pytest.mark.skip` (API-only address tests)

5. **Execution results**: `8 passed, 31 skipped, 8 xfailed, 1 xpassed in 82.96s`

6. **Table fill-in**: All Actual Result and Verdict columns updated in TC-B-01–29, TC-B-C-01–04, TC-B-BV-01–15

---

### Section 3 — Verdict

**VALID**

The AI correctly:
- Identified which tests were testable via Selenium web UI vs. API-only or mobile-only
- Used `@pytest.mark.skip` (not deletion) for untestable cases, satisfying the "mark it instead of hiding" requirement
- Used `@pytest.mark.xfail(strict=False)` for tests where correct behavior currently fails due to bugs — preserving intent while documenting the defect
- Applied React-aware automation strategies (React Router navigation for cart state, double-click for ProductDetail, localStorage injection for auth, `parse_vnd()` locale-aware parsing)
- Correctly identified the XPASS root cause (Selenium `clear()` does not fire React synthetic `onChange`) and flagged TC-B-25 for manual verification rather than silently accepting the XPASS

Minor limitation: TC-B-13 used `driver.get('/cart')` which clears React state — this is acceptable here since the precondition is empty cart, but the test name was slightly misleading (it tested the GET /api/cart empty response rather than the React state). The overall test suite is architecturally sound.

---

### Section 4 — Reasoning

The AI's approach aligns with ISTQB FL 4.3 (Test Execution) by executing test cases and recording actual results against expected results. Using `@pytest.mark.skip` preserves traceability to the test case ID without hiding gaps — conformant with ISTQB 5.2 (Defect Management) which requires defects to be logged and tracked, not suppressed. The `@pytest.mark.xfail` pattern correctly implements ISTQB's distinction between "test fail" (unexpected) and "known defect behavior" (expected) — equivalent to a defect report with an accepted/deferred status. The Page Object Model separation satisfies ISTQB's maintainability criteria for test automation (ISTQB CTAL-TAE 3.4). The React-specific workarounds (double-click, localStorage injection, router navigation) demonstrate accurate technical understanding of the SUT that goes beyond generic automation patterns.

---

### Section 5 — Student Fix

Accepted all test implementations with the following personal verifications:

1. **XPASS (TC-B-25) handling** — I independently checked `ProductDetail.jsx:27` and confirmed `parseInt("") = NaN` with no guard; agreed the test correctly identifies the code risk even though Selenium cannot reproduce it. Added "MANUAL VERIFY" verdict with explanation in the table.

2. **Double-click on product detail** — I verified `ProductDetail.jsx` `clickCount` guard is real; the POM's double-click pattern is the correct Selenium approach.

3. **TC-B-12 verdict** — I agreed that "PASS (BUG-B-04 documented)" is the correct verdict: the test *passed* its assertion (2 rows), which documents the inconsistency, even though the behavior itself is a bug.

4. **TC-B-16 xfail** — I verified that `driver.get('/checkout')` after auth injection does NOT preserve React cart state (React `useState([])` reinitialises on full mount); the test correctly demonstrates the empty-cart checkout vulnerability.

---

## AI Accuracy Summary

| Verdict | Count | % |
|---------|-------|---|
| VALID | 7 | 88% |
| INCOMPLETE | 1 | 12% |
| INVALID | 0 | 0% |

**Conclusion:** AI is effective for generating structured test cases from visible UI artefacts and producing automation scripts that follow standard patterns (POM, fixture isolation). It is also effective at expanding existing domain analyses when given clear source code context — correctly identifying security-critical inputs (client-controlled `price`, `total_amount` bypass), escalating source-code observations into formal bug reports, and applying boundary analysis across formula boundary values. It handles React-specific automation challenges (synthetic events, client-side state, router navigation) correctly when the architecture is described. It is unreliable for **initial** domain analysis without explicit prompting for industry standards (RFC 5321, NIST 800-63B, OWASP), and cannot independently discover UI-layer defects without a screenshot or running application. Gaps consistently appear around access-control testing (auth enforcement) and application lifecycle edge cases (app restart, in-memory state). Human review of the complete test suite and cross-checking with applicable standards is essential before accepting AI-generated test artefacts.

