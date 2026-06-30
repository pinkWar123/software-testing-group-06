"""
tests/test_coupon_ui.py
FR-17: Coupon Management (CRUD) — UI Test Suite (TC-C-UI-01 to TC-C-UI-16)

Scope   : Admin frontend (localhost:5174) — "Quản lý Mã Giảm Giá" tab
Platform: Selenium 4 + pytest

UI path:
  http://localhost:5174  →  login (inject adminToken via localStorage)
                         →  sidebar "Mã Giảm Giá"
                         →  coupon create form + coupon table

Test classification:
  PASS   — asserts correct / current behaviour; expected to succeed
  XFAIL  — asserts the CORRECT expectation; currently fails due to a documented bug
  SKIP   — cannot be verified via UI (API-only tests)

Architecture notes (from App.jsx):
  - Admin app checks localStorage.getItem("adminToken") on mount.
  - Error handling: form submission errors surfaced as browser alert() dialogs.
  - Expired coupon rendering: new Date(c.expired_at) < new Date() → red "Hết hạn" span.
  - XSS safety: coupon code rendered as JSX {c.code} — auto-escaped, no raw HTML.
  - Duplicate code: backend returns 500 (unhandled UNIQUE constraint → BUG-C-02).
"""

import time

import pytest
from assertpy import assert_that
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import (
    ADMIN_URL, ADMIN_EMAIL, ADMIN_PASSWORD,
    db_create_coupon, db_delete_coupon_by_code, db_get_coupon_by_code,
)
from pages.admin_coupon_page import AdminCouponPage

# ── Unique test-code prefix to avoid collisions with seed data ─────────────────
_P = "TC"   # prefix; combined with test-specific suffix for each test

# ── Module-level coupon cleanup ────────────────────────────────────────────────

TEST_CODES = [
    f"{_P}01", f"{_P}02", f"{_P}05A", f"{_P}06A", f"{_P}07A",
    f"{_P}08A", f"{_P}09A", f"{_P}10A", f"{_P}12A", f"{_P}13A",
    f"{_P}14A", f"{_P}16A", f"{_P}16B", "MAX100", "OVER101", "ZERO",
    "NEG1", "PAST1", "ZERO2", "NEWTEST", "XSSCODE", "DUPTEST",
    "<SCRIPT>ALERT(1)</SCRIPT>",
]


@pytest.fixture(autouse=True)
def _cleanup_test_coupons():
    db_delete_coupon_by_code(*TEST_CODES)
    yield
    db_delete_coupon_by_code(*TEST_CODES)


# ── Helper: navigate admin_driver directly to coupons tab ─────────────────────

def open_coupons(admin_driver) -> AdminCouponPage:
    page = AdminCouponPage(admin_driver)
    page.navigate_to_coupons_tab()
    return page


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-01 — Submit create form with ALL fields empty
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_01_all_fields_empty(admin_driver):
    """TC-C-UI-01: Clicking 'Tạo mã' with all fields blank → HTML5 required blocks submission.

    Expected: Form not submitted; no API call; table unchanged; no new row added.
    Verdict: PASS — HTML5 required attributes on code, discount_value, and expired_at fields
             prevent submission; the browser shows native validation tooltip.
    """
    page = open_coupons(admin_driver)
    initial_codes = page.get_coupon_codes_in_table()

    page.click_submit()
    time.sleep(0.5)

    # No alert should appear (form blocked by HTML5 required before any API call)
    alert_text = page.dismiss_alert(timeout=1.5)
    codes_after = page.get_coupon_codes_in_table()

    assert_that(alert_text).described_as(
        "TC-C-UI-01: No error alert should appear — HTML5 required blocks before API call"
    ).is_none()
    assert_that(codes_after).described_as(
        "TC-C-UI-01: Table row count must not change after empty-form submission"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-02 — Submit with code field empty only
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_02_code_field_empty(admin_driver):
    """TC-C-UI-02: Code blank; other fields filled → HTML5 required on code blocks submit.

    Expected: Error on code field; form not submitted; no new row.
    Verdict: PASS — code input has 'required' attribute; browser blocks submission.
    """
    page = open_coupons(admin_driver)

    # Fill everything except code
    page.set_type("fixed")
    page.set_discount_value(50000)
    page.set_min_order(0)
    page.set_expired_at("2099-12-31")
    page.set_max_uses(1)
    # Do NOT call set_code() — leave it empty

    initial_codes = page.get_coupon_codes_in_table()
    page.click_submit()
    time.sleep(0.5)

    alert_text = page.dismiss_alert(timeout=1.5)
    codes_after = page.get_coupon_codes_in_table()

    assert_that(alert_text).described_as(
        "TC-C-UI-02: No alert — HTML5 required on code field blocks before API call"
    ).is_none()
    assert_that(codes_after).described_as(
        "TC-C-UI-02: Table unchanged; empty code was rejected by browser"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-03 — Type dropdown only allows valid options
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_03_type_dropdown_options(admin_driver):
    """TC-C-UI-03: Verify the Loại dropdown contains only 'percent' and 'fixed'.

    Expected: Exactly 2 options — 'Phần trăm (%)' (value=percent) and 'Số tiền cố định' (value=fixed).
    Verdict: PASS — dropdown constrains type; invalid types like 'cashback' are unreachable via UI.
    """
    page = open_coupons(admin_driver)
    options = page.get_type_options()

    assert_that(options).described_as(
        "TC-C-UI-03: Type dropdown must have exactly 2 options (percent and fixed)"
    ).is_equal_to(["percent", "fixed"])


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-04 — Switch type — placeholder updates
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_04_type_switch_placeholder(admin_driver):
    """TC-C-UI-04: Switch type percent→fixed; verify discount_value placeholder changes.

    Expected: percent placeholder = 'Giá trị % (VD: 10)'; fixed = 'Số tiền (VD: 50000)'.
    Verdict: PASS — React re-renders placeholder on type change.
    """
    page = open_coupons(admin_driver)

    page.set_type("percent")
    placeholder_percent = page.get_discount_value_placeholder()

    page.set_type("fixed")
    placeholder_fixed = page.get_discount_value_placeholder()

    assert_that(placeholder_percent).described_as(
        "TC-C-UI-04: percent type placeholder"
    ).contains("Giá trị %")
    assert_that(placeholder_fixed).described_as(
        "TC-C-UI-04: fixed type placeholder"
    ).contains("Số tiền")


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-05 — Create percent coupon with discount_value=100 (BVA on-point max)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_05_create_percent_100(admin_driver):
    """TC-C-UI-05: discount_value=100, type=percent → coupon created; appears in table as '100%'.

    Expected: Form accepted; row shows '100%'; no validation error.
    Verdict: PASS — backend has no range validation; value=100 stored and displayed.
    Note: Applying this coupon would produce a catastrophic negative amount (BUG-C-01).
    """
    page = open_coupons(admin_driver)
    page.submit_form(
        code="MAX100", type_="percent", discount_value=100,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)

    assert_that(alert_text).described_as(
        "TC-C-UI-05: No error alert for value=100"
    ).is_none()
    appeared = page.wait_for_row_present("MAX100", timeout=4)
    assert_that(appeared).described_as(
        "TC-C-UI-05: Coupon MAX100 must appear in table after creation"
    ).is_true()


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-06 — discount_value=101 (BVA off-point over 100%)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(
    reason="BUG: No server-side or client-side range validation for discount_value. "
           "101 is accepted and stored — form should reject values > 100 for percent type.",
    strict=False,
)
@pytest.mark.coupon_ui
def test_TC_C_UI_06_discount_over_100(admin_driver):
    """TC-C-UI-06: discount_value=101 (invalid percentage) → form should reject.

    Expected (correct): Validation error 'Value must be between 1 and 100'.
    Actual: Form submits; coupon stored with value=101 — no range enforcement.
    Verdict: XFAIL → BUG-C-01 (cascading: applying would produce even more negative amounts).
    """
    page = open_coupons(admin_driver)
    initial_codes = page.get_coupon_codes_in_table()

    page.submit_form(
        code="OVER101", type_="percent", discount_value=101,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)
    codes_after = page.get_coupon_codes_in_table()

    # Correct expectation: form rejected (alert shown OR table unchanged)
    assert_that(alert_text).described_as(
        "TC-C-UI-06: Expected validation error for discount_value > 100"
    ).is_not_none()
    # Or table should not gain a new row
    assert_that(codes_after).described_as(
        "TC-C-UI-06: Table should not gain OVER101 row"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-07 — discount_value=0 (BVA off-point below min)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(
    reason="BUG: discount_value=0 accepted by backend — a zero-discount coupon is meaningless. "
           "No client-side or server-side validation prevents creation.",
    strict=False,
)
@pytest.mark.coupon_ui
def test_TC_C_UI_07_discount_zero(admin_driver):
    """TC-C-UI-07: discount_value=0 → form should reject (no discount is meaningless).

    Expected (correct): Validation error; form not submitted.
    Actual: Backend accepts value=0; coupon created with 0% discount.
    Verdict: XFAIL → BUG.
    """
    page = open_coupons(admin_driver)
    initial_codes = page.get_coupon_codes_in_table()

    page.submit_form(
        code="ZERO", type_="percent", discount_value=0,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)
    codes_after = page.get_coupon_codes_in_table()

    assert_that(alert_text).described_as(
        "TC-C-UI-07: Expected validation error for discount_value=0"
    ).is_not_none()
    assert_that(codes_after).described_as(
        "TC-C-UI-07: ZERO should not appear in table"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-08 — Negative discount_value
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(
    reason="BUG: Negative discount_value accepted — no min attribute on number input; "
           "backend stores the negative value which would INCREASE the order total when applied.",
    strict=False,
)
@pytest.mark.coupon_ui
def test_TC_C_UI_08_negative_discount(admin_driver):
    """TC-C-UI-08: discount_value=-10 → form should reject negative discount.

    Expected (correct): HTML5 min validation or server rejects; form not submitted.
    Actual: discount_value input has no min attribute → accepts -10; backend stores it.
    Verdict: XFAIL → BUG (negative discount would ADD to order total).
    """
    page = open_coupons(admin_driver)
    initial_codes = page.get_coupon_codes_in_table()

    page.submit_form(
        code="NEG1", type_="fixed", discount_value=-10,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)
    codes_after = page.get_coupon_codes_in_table()

    assert_that(alert_text).described_as(
        "TC-C-UI-08: Expected validation error for negative discount_value"
    ).is_not_none()
    assert_that(codes_after).described_as(
        "TC-C-UI-08: NEG1 should not appear in table"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-09 — Past date via date picker
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_09_past_date_accepted(admin_driver):
    """TC-C-UI-09: Select past date (2020-01-01) → browser does NOT prevent it;
    backend creates coupon with past expiry; coupon immediately expired on creation.

    Expected (best practice): Browser or server should reject past expiry dates at creation.
    Actual: No min attribute on date input → past date accepted; coupon created immediately expired.
    Verdict: DOCUMENTED as usability/logic gap — server allows creation of already-expired coupons.
    """
    page = open_coupons(admin_driver)

    page.submit_form(
        code="PAST1", type_="fixed", discount_value=5000,
        min_order=0, expired_at="2020-01-01", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)

    # Verify no crash (alert would indicate error)
    # Either the coupon is created (gap documented) or it's rejected (best practice met)
    row_appeared = page.wait_for_row_present("PAST1", timeout=4)

    # Document actual behaviour:
    # No browser-side past-date prevention → coupon created with past expiry
    assert_that(alert_text).described_as(
        "TC-C-UI-09: No error on past date submission — server accepts it (usability gap)"
    ).is_none()
    assert_that(row_appeared).described_as(
        "TC-C-UI-09: PAST1 coupon created with past expiry date — no creation-time validation"
    ).is_true()


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-10 — max_uses_per_user=0 (BVA off-point; min="1" attribute)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_10_max_uses_zero_blocked(admin_driver):
    """TC-C-UI-10: max_uses_per_user=0 → HTML5 min='1' attribute blocks submission.

    Expected: Form not submitted; HTML5 validation tooltip shown.
    Verdict: PASS — the max_uses input has min='1'; browser rejects 0 on form submit.
    """
    page = open_coupons(admin_driver)
    initial_codes = page.get_coupon_codes_in_table()

    page.set_code("ZERO2")
    page.set_type("fixed")
    page.set_discount_value(5000)
    page.set_min_order(0)
    page.set_expired_at("2099-12-31")
    # Set max_uses to 0 — bypasses React state to set raw DOM value
    max_field = admin_driver.find_element(
        By.CSS_SELECTOR, "input[placeholder='Số lần dùng tối đa/người']"
    )
    admin_driver.execute_script("arguments[0].value = '0'", max_field)

    page.click_submit()
    time.sleep(0.5)

    alert_text = page.dismiss_alert(timeout=1.5)
    codes_after = page.get_coupon_codes_in_table()

    assert_that(alert_text).described_as(
        "TC-C-UI-10: No alert — HTML5 min=1 blocks before API call"
    ).is_none()
    assert_that(codes_after).described_as(
        "TC-C-UI-10: Table unchanged; max_uses=0 rejected by HTML5 min=1"
    ).is_equal_to(initial_codes)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-11 — Expired coupon displays "Hết hạn" in red
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_11_expired_coupon_shows_red_badge(admin_driver):
    """TC-C-UI-11: Coupon with past expired_at renders 'Hết hạn' in red in the table.

    Pre-condition: EXPIRED coupon with expired_at='2020-01-01' exists (seed data).
    Expected: Table row for EXPIRED shows <span class='text-red-500'>Hết hạn</span>.
    Verdict: PASS — App.jsx conditionally renders red badge when new Date(expired_at) < new Date().
    """
    page = open_coupons(admin_driver)

    expiry_text = page.get_expiry_cell_text("EXPIRED")

    assert_that(expiry_text).described_as(
        "TC-C-UI-11: EXPIRED coupon must show 'Hết hạn' in the expiry column"
    ).is_equal_to("Hết hạn")

    badge_count = page.count_expired_badges()
    assert_that(badge_count).described_as(
        "TC-C-UI-11: At least one red 'Hết hạn' badge must be visible"
    ).is_greater_than(0)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-12 — Newly created coupon appears immediately in table
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_12_create_coupon_appears_in_table(admin_driver):
    """TC-C-UI-12: Fill form completely → click 'Tạo mã' → new row appears immediately.

    Input: code=NEWTEST, type=fixed, value=50000, min=100000, date=2099-12-31, max=1.
    Expected: Success (no alert); NEWTEST row visible in table with correct column values.
    Verdict: PASS — fetchData() called on success; React re-renders table with new row.
    """
    page = open_coupons(admin_driver)

    page.submit_form(
        code="NEWTEST", type_="fixed", discount_value=50000,
        min_order=100000, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=2)
    appeared   = page.wait_for_row_present("NEWTEST", timeout=5)

    assert_that(alert_text).described_as(
        "TC-C-UI-12: No error alert on valid coupon creation"
    ).is_none()
    assert_that(appeared).described_as(
        "TC-C-UI-12: NEWTEST must appear in the coupon table after creation"
    ).is_true()

    row = page.get_row_for_code("NEWTEST")
    cells = row.find_elements(By.TAG_NAME, "td")
    assert_that(cells[1].text.strip()).described_as(
        "TC-C-UI-12: Loại column must show 'Cố định' for fixed type"
    ).is_equal_to("Cố định")
    assert_that("50,000" in cells[2].text or "50000" in cells[2].text).described_as(
        "TC-C-UI-12: Giá trị column must show 50,000 ₫"
    ).is_true()
    assert_that(cells[4].text.strip()).described_as(
        "TC-C-UI-12: Hết hạn column must show 2099-12-31"
    ).is_equal_to("2099-12-31")


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-13 — Delete coupon via Xóa button
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_13_delete_coupon(admin_driver):
    """TC-C-UI-13: Click the red 'Xóa' button for a coupon → row disappears from table.

    Pre-condition: Create a test coupon via DB, navigate to coupons tab.
    Expected: Row removed from table immediately after click; no confirmation dialog.
    Verdict: PASS — axios.delete() called; fetchData() updates React state; row removed.
    """
    db_create_coupon("TC13A", type_="fixed", discount_value=5000, expired_at="2099-12-31")

    # Refresh so admin panel re-fetches coupons from DB (fetchData is called on token load)
    admin_driver.refresh()
    WebDriverWait(admin_driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(),'Mã Giảm Giá')]"))
    )
    page = open_coupons(admin_driver)
    assert_that(page.is_code_in_table("TC13A")).described_as(
        "TC-C-UI-13: TC13A must be present in table before delete"
    ).is_true()

    page.delete_coupon_by_code("TC13A")
    gone = page.wait_for_row_gone("TC13A", timeout=5)

    assert_that(gone).described_as(
        "TC-C-UI-13: TC13A row must be removed from table after clicking Xóa"
    ).is_true()


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-14 — XSS payload in coupon code — safe rendering in table
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_14_xss_in_code_safe_rendering(admin_driver):
    """TC-C-UI-14: Type XSS payload in code field → coupon created; table renders literal text.

    Input: code='<SCRIPT>ALERT(1)</SCRIPT>' (uppercased by React onChange).
    Expected: No alert dialog fires after table renders; code shown as literal text.
    Verdict: PASS — React JSX {c.code} auto-escapes HTML; no script executes.
    Note: The API auto-uppercases the code, so it's stored as the uppercase version.
    """
    xss_input = "<script>alert(1)</script>"
    page = open_coupons(admin_driver)

    page.submit_form(
        code=xss_input, type_="fixed", discount_value=1,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    # Wait a moment; if XSS fires, an alert appears — we should NOT see one
    time.sleep(1)
    alert_text = page.dismiss_alert(timeout=1.5)

    # No browser alert dialog should have fired (XSS payload did not execute)
    assert_that(alert_text).described_as(
        "TC-C-UI-14: No alert should appear — XSS payload must not execute in the table"
    ).is_none()

    # The table should show the code as literal text (uppercased by React)
    codes = page.get_coupon_codes_in_table()
    xss_upper = xss_input.upper()
    assert_that(any(xss_upper in c or "SCRIPT" in c for c in codes)).described_as(
        "TC-C-UI-14: XSS payload stored and rendered as literal text (not executed)"
    ).is_true()


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-15 — Navigate to admin page without login → login form shown
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_15_unauthenticated_access(driver):
    """TC-C-UI-15: Navigate to admin URL without token → login form is shown; admin content hidden.

    Pre-condition: No adminToken in localStorage.
    Expected: Admin login form visible (h2 'Admin Login'); sidebar NOT visible.
    Verdict: PASS — App.jsx checks !token → renders login form conditionally; admin panel hidden.
    Note: The app does client-side conditional rendering, not a server-side redirect.
    """
    driver.get(ADMIN_URL)
    wait = WebDriverWait(driver, 8)

    # Login form should be shown
    login_heading = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Admin Login')]"))
    )
    assert_that(login_heading.is_displayed()).described_as(
        "TC-C-UI-15: 'Admin Login' heading must be visible when not authenticated"
    ).is_true()

    # Sidebar with coupon nav must NOT be visible
    sidebar_items = driver.find_elements(By.XPATH, "//li[contains(text(),'Mã Giảm Giá')]")
    assert_that(len(sidebar_items)).described_as(
        "TC-C-UI-15: Coupon sidebar item must not be visible to unauthenticated user"
    ).is_equal_to(0)


# ══════════════════════════════════════════════════════════════════════════════
# TC-C-UI-16 — Duplicate coupon code → error message shown on UI (BUG-C-02)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.coupon_ui
def test_TC_C_UI_16_duplicate_code_error_shown(admin_driver):
    """TC-C-UI-16 (Part A): Duplicate code → an error alert IS shown to the user.

    Pre-condition: BIGBUY coupon already exists in seed data.
    Expected: Any error alert appears after submitting a duplicate code.
    Verdict: PASS — alert() is called by the admin frontend's catch block.
    """
    page = open_coupons(admin_driver)

    page.submit_form(
        code="BIGBUY", type_="fixed", discount_value=50000,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=4)

    assert_that(alert_text).described_as(
        "TC-C-UI-16: An error alert must appear when submitting a duplicate coupon code"
    ).is_not_none()


@pytest.mark.xfail(
    reason="BUG-C-02: Duplicate code causes unhandled 500; backend returns raw SQLite "
           "UNIQUE constraint error instead of a 409 Conflict with a user-friendly message. "
           "Alert shows: 'SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code'",
    strict=True,
)
@pytest.mark.coupon_ui
def test_TC_C_UI_16_duplicate_code_friendly_message(admin_driver):
    """TC-C-UI-16 (Part B — BUG-C-02): Error alert text should be user-friendly.

    Expected (best practice): Alert contains 'Mã coupon đã tồn tại' (code already exists).
    Actual: Alert contains raw SQLite constraint error — '...UNIQUE constraint failed: coupons.code'.
    Verdict: XFAIL (strict) → BUG-C-02 confirmed; raw server error exposed to admin user.
    """
    page = open_coupons(admin_driver)

    page.submit_form(
        code="BIGBUY", type_="fixed", discount_value=50000,
        min_order=0, expired_at="2099-12-31", max_uses=1
    )
    alert_text = page.dismiss_alert(timeout=4) or ""

    assert_that(alert_text.lower()).described_as(
        "TC-C-UI-16 BUG-C-02: Alert should contain friendly message, not raw SQLite error"
    ).contains("đã tồn tại")
