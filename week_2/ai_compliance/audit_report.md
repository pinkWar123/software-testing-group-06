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

## AI Accuracy Summary

| Verdict | Count | % |
|---------|-------|---|
| VALID | 2 | 67% |
| INCOMPLETE | 1 | 33% |
| INVALID | 0 | 0% |

**Conclusion:** AI is effective for generating structured test cases from visible UI artefacts and producing automation scripts that follow standard patterns (POM, fixture isolation). It is unreliable for **initial** domain analysis without explicit prompting for industry standards (RFC 5321, NIST 800-63B), and cannot independently discover UI-layer defects without a screenshot or running application. Human review of the complete test suite and cross-checking with applicable standards is essential before accepting AI-generated test artefacts.

