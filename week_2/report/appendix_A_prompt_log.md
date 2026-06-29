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
