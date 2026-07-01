# Appendix A — Prompt Log
## HW02 — Domain Testing on EShop

> **Format for each entry:**
> ```
> ## [HH:MM dd/mm/yyyy] — [Tool Name]
> **Purpose**: [which HW requirement this served]
> **Prompt**:
> > [full prompt verbatim]
>
> **Artifact produced**: [name/description of output]
>
> ---
> ```

> ⚠️ Every real prompt sent to any AI tool must be logged here with real timestamps.
> Do NOT use AI to generate this log — timestamps must reflect actual sessions.

---

## 21:29 01/07/2026 — GPT-5 Codex
**Purpose**: R1 – Refine Feature D (Pool D) so it covers one concrete mobile feature only; rewrite domain analysis and BVA for mobile add-to-cart quantity input
**Prompt**:
> "$qa-test-planner I'm writing the report for my homework in week_2/report/report.md , and working on feature D for mobile. Actually, mobile app has many features, so we only need to pick one and then perform domain and boundary analysis for it. So help me to choose one feature, then perform your expertise to do analysis, update the analysis and test cases accordingly"

**Artifact produced**: Reworked Section 5 (Feature D) of `week_2/report/report.md` to focus on a single coherent mobile feature: **Mobile Add-to-Cart Quantity Input**. Updated the Feature Selection table and TOC label. Removed mixed mobile cases unrelated to the chosen feature (login, coupon, restart, checkout-total cases). Rebuilt the domain model around `quantity_text`, derived `parsed_quantity`, derived `effective_quantity`, and `stock_relation`. Added 12 domain test cases (TC-D-01 to TC-D-12), 3 constraint-based test cases (TC-D-C-01 to TC-D-C-03), and 10 BVA test cases (TC-D-BV-01 to TC-D-BV-10). Reframed Actual Result/Verdict values to distinguish **static code-trace evidence** from true executed mobile tests, and consolidated the bug list to 3 quantity-input defects: silent normalization with no feedback, decimal truncation, and missing upper-bound/stock validation.

---

## 22:05 01/07/2026 — GPT-5 Codex
**Purpose**: R3 – Implement and execute Selenium tests for Feature D through the Expo web build of the mobile app; replace analysis-only rows with observed results where verifiable
**Prompt**:
> "Now you should apply $webapp-selenium-testing to help me write and execute selenium tests for the test cases. You can reference to how the current tests work in artifacts folder. Then fill into the test cases table. In case you can't verify a test case, let me know instead of assuming."

**Artifact produced**: Added Selenium automation for Feature D under `week_2/artifacts/selenium/` using the existing Python/pytest stack: new page object `pages/mobile_app_page.py`, new test module `tests/test_mobile_quantity.py`, and marker `mobile_quantity` in `pytest.ini`. Started the backend and Expo web target (`frontend-mobile` on `http://localhost:8082`) and executed the suite with `python3 -m pytest tests/test_mobile_quantity.py -q`. Final result: **21 passed, 2 skipped**. Updated Section 5 of `week_2/report/report.md` so TC-D-01..10, TC-D-C-01..03, and TC-D-BV-01..07 / 10 now contain **observed Selenium results** instead of code-inference placeholders. Left stock-dependent cases (TC-D-11, TC-D-12, TC-D-BV-08, TC-D-BV-09) explicitly marked **SKIP / not verifiable** because the mobile UI does not expose or validate stock in the add-to-cart path.


## 21:55 22/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R1 – Domain testing & BVA for Feature A (FR-02: Login and Account Lockout); correct existing TCs and add RFC 5321 / NIST 800-63B constraint cases
**Prompt**:
> "The homework assignment is in @homework.md. Check the current state of @week_2/report/report.md. First we need to define test cases for login and account lockout. I provided you a screenshot of the login screen. Check the existing test cases, modify or correct them if needed, and provide me more test cases following Domain testing and boundary value analysis techniques."
>
> *(Follow-up after screenshot was provided):*
> "That can be an intentional mistake for software testing course. Don't check the code, just apply your expertise."

**Artifact produced**: Updated Section 2 (Feature A) of `report.md` — corrected domain table (username rename), 20 domain TCs (TC-A-01 to TC-A-20), 22 BVA TCs (TC-A-BV-01 to TC-A-BV-22), 16 constraint TCs (TC-A-C-01 to TC-A-C-16); 2 UI bugs found (BUG-A-01, BUG-A-02)

---

## 11:09 23/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R3 – Test automation; generate Selenium/pytest test scripts for Feature A test cases
**Prompt**:
> "help me write a selenium script to test these test cases automatically. Also, the test case doesn't cover constraints, like maximum length of string, malformed email, and so on. Don't just base on the code, follow the best practice constraints for these field"

**Artifact produced**: Complete Selenium test suite at `week_2/artifacts/selenium/` — `requirements.txt`, `pytest.ini`, `conftest.py` (DB fixtures), `pages/login_page.py` (POM), `tests/test_login_domain.py` (20 tests), `tests/test_login_bva.py` (22 tests), `tests/test_login_constraints.py` (16 tests); 58 tests collected

---

## 15:12 23/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R3 – Test execution; run all 58 Feature A Selenium tests and fill Actual Result + Verdict columns in report
**Prompt**:
> "help me execute these test cases and then fill into the report"

**Artifact produced**: Full test execution results — 44 PASS, 2 FAIL, 12 PASS*; Actual Result and Verdict columns populated for all TCs in Section 2; Section 2.3 AI Gap Analysis (5 gaps) and Section 2.4 Bug Report (6 bugs: BUG-A-01 to BUG-A-06) filled

---

## 15:01 26/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R1 – Domain testing & BVA for Feature B (FR-07: Shopping Cart); QA audit and execution plan
**Prompt**:
> "Use the skill tool to invoke the 'breakdown-test' skill, then follow the skill's instructions to help with: /plan apply your skill as an expert QA engineer, help me to adjust/correct/add test cases to the second feature of @week_2/report/report.md - shopping cart. Then generate a comprehensive plan on what you may execute"

**Artifact produced**: QA gap analysis of existing Feature B test suite (7 identified problems) and structured 7-task execution plan covering domain corrections, new TCs, BVA, AI Gap Analysis, and Bug Report

---

## 17:18 26/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R1 – Domain testing & BVA for Feature B (FR-07: Shopping Cart); execute all corrections and additions
**Prompt**:
> "OK proceed with it."

**Artifact produced**: Updated Section 3 (Feature B) of `report.md` — corrected TC-B-03/04/08/09/12 expected results, `price` domain (D-PR1–D-PR4) added, TC-B-13 to TC-B-22 (10 new TCs), 4 OWASP constraint TCs, Section 3.2 BVA (15 TCs), Section 3.3 AI Gap Analysis (8 gaps), Section 3.4 Bug Report (5 bugs: BUG-B-01 to BUG-B-05 including 2 Critical security bugs)

---

## 21:54 26/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R1 – Domain testing & BVA for Feature C (FR-17: Coupon Management) and Feature D (Mobile App); fill all empty sections
**Prompt**:
> "Continue with the next section"

**Artifact produced**: Updated Sections 4 and 5 of `report.md` — Feature C: expanded domain tables (8 tables), TC-C-14 to TC-C-23 + 3 OWASP constraint TCs, Section 4.2 BVA (15 TCs), Section 4.3 AI Gap Analysis (7 gaps), Section 4.4 Bug Report (4 bugs: BUG-C-01 Critical); Feature D: expanded domain tables, TC-D-15 to TC-D-21 + 3 constraint TCs, Section 5.2 BVA (12 TCs), Section 5.3 AI Gap Analysis (6 gaps), Section 5.4 Bug Report (4 bugs: BUG-D-01 to BUG-D-04)

---

## 13:15 29/06/2026 — Claude Opus 4.8 (Claude Code CLI)
**Purpose**: R1 – Critical review of Feature B (FR-07: Shopping Cart) domain testing & BVA against the actual SUT source; adjust/add/modify
**Prompt**:
> "/qa-test-planner /qa-manual-istqb There are already some predefined test cases for feature B as long as domain and boudnary analysis. Use your expertise to bring a critical thinking on these output, and adjust/add/modify if needed"

**Artifact produced**: Revised Section 3 (Feature B) of `report.md` after tracing the real cart call graph (backend/server.js + frontend-web + frontend-mobile). Corrected the architecture framing (cart is client-side React state; `/api/cart` is orphaned dead code); rewrote Step 1; split `auth_state` into D-Auth1/2/3 (401 vs 403); corrected TC-B-12 (frontend-dependent duplicate handling) and TC-B-14 (add-to-cart needs no auth); added BVA scope correction; added 7 UI-reachable test cases (TC-B-23–29) covering the editable-checkout-total exploit, NULL shipping_address, web NaN/negative quantity, mobile off-by-one qty editor, refresh-clears-cart, mobile dropped-last-item; added 5 AI gap-analysis items (9–13); upgraded/corrected the bug table to BUG-B-01–08 (BUG-B-02 re-scoped to UI-exploitable Critical; BUG-B-04 root cause fixed; BUG-B-05 downgraded; BUG-B-06/07/08 new).

---

## 14:00 29/06/2026 — Claude Opus 4.8 (Claude Code CLI)
**Purpose**: R2 – Selenium test automation for Feature B (FR-07: Shopping Cart); execute all testable TCs and fill Actual Result/Verdict columns
**Prompt**:
> "help me to write selenium script to execute the test cases of feature B. Then fill into the tables. In case you encounter a test case that can't verify or it runs wrong compared to our expectation, you should mark it instead of hiding it, which allows me to verify manually later."

**Artifact produced**: (1) New Selenium test files: `week_2/artifacts/selenium/tests/test_cart_domain.py` (35 tests, TC-B-01 to TC-B-29) and `week_2/artifacts/selenium/tests/test_cart_bva.py` (15 tests, TC-B-BV-01 to TC-B-BV-15). (2) New POM classes: `pages/home_page.py`, `pages/product_detail_page.py`, `pages/cart_page.py`, `pages/checkout_page.py`. (3) Extended `conftest.py` with cart-specific helpers: `get_api_token()`, `inject_auth_token()`, `db_get_last_order()`, `db_delete_test_orders()`, `logged_in_driver` fixture, `clean_orders` fixture. (4) Updated `pytest.ini` with `cart_domain` and `cart_bva` markers. (5) Test execution results: `8 passed, 31 skipped, 8 xfailed, 1 xpassed in 82.96s`. (6) Filled all Actual Result and Verdict columns in all four Feature B test tables (TC-B-01–29, TC-B-C-01–04, TC-B-BV-01–15) in `report.md` based on execution results, with skip/xfail/manual-verify markings where tests could not be executed via Selenium web UI.

---

## 22:59 29/06/2026 — Claude Sonnet 4.6 (Claude Code CLI)
**Purpose**: R2 – Execute remaining N/A API-only test cases for Feature B (FR-07: Shopping Cart) via curl; fill actual results
**Prompt**:
> "Now help me to execute curls to test for the remaining N/A cases due to API tests of the feature"

**Artifact produced**: Executed 18 curl commands against `http://localhost:3000` covering: POST /api/cart (TC-B-01 to TC-B-04, TC-B-18, TC-B-19, TC-B-21, TC-B-C-01, TC-B-C-04, TC-B-BV-06, TC-B-BV-07, TC-B-BV-08), GET /api/cart without token (TC-B-C-03), POST /api/checkout (TC-B-10, TC-B-11, TC-B-17, TC-B-22, TC-B-BV-12, TC-B-BV-13, TC-B-BV-14, TC-B-BV-15). Updated all corresponding Actual Result and Verdict cells in `report.md`. Key findings: BUG-B-01 confirmed (qty 0/-1 accepted by server), BUG-B-02 confirmed again via API (total=1 accepted), BUG-B-05 confirmed (price=0/-50000 accepted), empty/null shipping_address accepted (BUG-B-06 reinforced), TC-B-C-03 PASS (401 returned correctly), XSS stored verbatim in DB (React UI safe due to JSX escaping but stored XSS risk remains for non-React consumers).

## 01:11 30/06/2026 — Claude Sonnet 4.6 (GitHub Copilot CLI)
**Purpose**: R1 – UI-based refinement of Feature C (FR-17: Coupon Management) domain testing & BVA; classify test cases as UI-executable vs API-only; add new UI test cases from screenshot analysis
**Prompt**:
> "Use the skill tool to invoke the 'qa-test-planner' skill, then follow the skill's instructions to help with: [image: copilot-image-5a5d1a.png] /plan Now you should help me to refine the test cases and domain and boundary value analysis for feature C in @week_2/report/report.md . Here we are focusing too much on the backend part, but now you should base on the UI I sent you to create a test plan on what you may execute and your analysis on domain and boundary, and what test cases you may wanna remove/correct/add"

**Artifact produced**: Updated Section 4 (Feature C) of `report.md` — (1) Added Step 1b: UI analysis table mapping all 6 form fields (code text input, type dropdown constrained to 2 options, discount_value number input with "VD: 10" placeholder, min_order number default 0, date picker dd/mm/yyyy, max_uses number default 1) and table structure (Mã/Loại/Giá trị/Đơn tối thiểu/Hết hạn/Giới hạn/người/Xóa). (2) Updated `discount_value` domain table with D-D5 (over 100 for percent), D-D6 (empty field), and UI-testable column. (3) Updated `expired_at` domain with date picker context note. (4) Updated BVA boundary table — percent range corrected to `[1, 100]` (on-points 1 and 100; off-points 0 and 101). (5) Added UI vs API-Only classification table for all TC-C-01 to TC-C-23 — flagged TC-C-12 (invalid type via dropdown not possible in UI) and TC-C-20 (decimal workaround API-only) for removal from UI plan; all apply-coupon TCs marked API-only. (6) Added 16 new UI test cases TC-C-UI-01 to TC-C-UI-16 covering: empty form submission, required-field validation, dropdown constraint, type-switch label update, percent value BVA (0/100/101), past date picker, negative values, expired "Hết hạn" red indicator, table refresh after create/delete, XSS rendering safety, unauthenticated page redirect, duplicate code UI error. (7) Added TC-C-BV-16 (value=100 on-point max) and TC-C-BV-17 (value=101 off-point over max) to BVA table. (8) Extended AI Gap Analysis with 3 new gaps: percent UI range not previously bounded (#8), entire UI coverage absent (#9), TC-C-12/TC-C-20 removal rationale (#10).

---

## 13:30 30/06/2026 — Claude Sonnet 4.6 (Claude Code CLI)
**Purpose**: R3 – Test automation; generate Selenium UI tests for Feature C (FR-17: Coupon Management) covering all 16 TC-C-UI cases; execute tests and fill Actual Results in report
**Prompt**:
> "help me to write selenium tests for UI tests of Feature C — FR-17: Coupon Management (CRUD) in @week_2/report/report.md then fill into the report and update audit-report /plog"

**Artifact produced**: (1) `week_2/artifacts/selenium/pages/admin_coupon_page.py` — Page Object Model for admin coupon management UI (admin panel at localhost:5174); locators for all form fields and table rows; stale-element-safe wait helpers; React native event dispatch fix for date input. (2) `week_2/artifacts/selenium/tests/test_coupon_ui.py` — 17 test functions (TC-C-UI-01 to TC-C-UI-16 + split TC-C-UI-16A/B); 13 PASS, 4 XFAIL. (3) Extended `conftest.py` with coupon DB helpers (`db_create_coupon`, `db_delete_coupon_by_code`, `db_get_coupon_by_code`), `inject_admin_token()`, and `admin_driver` fixture. (4) Filled all 16 TC-C-UI Actual Result and Verdict cells in `report.md` Section 4.1. (5) Added AI-02-10 entry to `audit_report.md`. Key execution findings: TC-C-UI-06/07/08 XFAIL (no discount_value range validation — BUG confirmed); TC-C-UI-16B XFAIL (raw SQLite UNIQUE error exposed — BUG-C-02 confirmed); TC-C-UI-09 PASS with gap note (past date accepted — no creation-time validation).

---
