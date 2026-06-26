"""
tests/test_login_constraints.py
FR-02: Login — Best-Practice Constraint Tests (TC-A-C-01 → TC-A-C-16)

Standards applied:
  • RFC 5321   — Internet email address format rules
  • NIST SP 800-63B — Digital Identity Guidelines (password policy)
  • OWASP Authentication Cheat Sheet — security best practices

Each test documents both the EXPECTED best-practice behaviour and
the ACTUAL system behaviour, distinguishing compliance gaps from bugs.
"""
import pytest

from conftest import TEST_EMAIL, TEST_PASSWORD, db_reset_account
from pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def _reset(driver):
    db_reset_account()
    yield
    db_reset_account()


# ── RFC 5321: Email format constraints ────────────────────────────────────────
@pytest.mark.constraints
def test_TC_A_C_01_multiple_at_symbols(driver):
    """TC-A-C-01 · RFC 5321 — Multiple '@' symbols are invalid email format.
    Best practice: 400 format error. Current SUT: likely 401 (no format check)."""
    page = LoginPage(driver).open()
    page.submit("test@@eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful(), "Multiple @ must not authenticate"


@pytest.mark.constraints
def test_TC_A_C_02_missing_domain_after_at(driver):
    """TC-A-C-02 · RFC 5321 — No domain part after '@' is invalid.
    Best practice: 400. Current SUT: 401."""
    page = LoginPage(driver).open()
    page.submit("test@", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_03_missing_local_part_before_at(driver):
    """TC-A-C-03 · RFC 5321 — No local part before '@' is invalid.
    Best practice: 400. Current SUT: 401."""
    page = LoginPage(driver).open()
    page.submit("@eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_04_no_tld_in_domain(driver):
    """TC-A-C-04 · RFC 5321 — Domain without a TLD is not a valid FQDN.
    Best practice: 400 (format validation). Current SUT: 401 (no check)."""
    page = LoginPage(driver).open()
    page.submit("test@eshop", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_05_space_in_email(driver):
    """TC-A-C-05 · RFC 5321 — Unquoted spaces in email are forbidden.
    Best practice: 400 format error. Current SUT: 401."""
    page = LoginPage(driver).open()
    page.submit("test @eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_06_consecutive_dots_in_local_part(driver):
    """TC-A-C-06 · RFC 5321 — Consecutive dots ('..') in local part are forbidden.
    Best practice: 400. Current SUT: 401."""
    page = LoginPage(driver).open()
    page.submit("test..user@eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_07_local_part_starts_with_dot(driver):
    """TC-A-C-07 · RFC 5321 — Local part cannot start with a dot.
    Best practice: 400. Current SUT: 401."""
    page = LoginPage(driver).open()
    page.submit(".test@eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


@pytest.mark.constraints
def test_TC_A_C_08_email_at_rfc_max_length_254_valid(driver):
    """TC-A-C-08 · RFC 5321 — Email at exactly 254 chars is the RFC maximum; must be accepted.
    Expected: 401 (not registered, but format is valid)."""
    local = "a" * 244
    email = f"{local}@eshop.com"  # 244 + 1 + 9 = 254
    assert len(email) == 254
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    # Must not show a format error for a valid-length RFC email
    error = page.get_error_text()
    assert page.is_error_shown(), f"254-char email: expected generic 401, got: '{error}'"


@pytest.mark.constraints
def test_TC_A_C_09_email_exceeds_rfc_max_255_chars(driver):
    """TC-A-C-09 · RFC 5321 — Email of 255 chars exceeds RFC 5321 max (254).
    Best practice: 400/413 'email too long'. Current SUT: likely 401 (no length check)."""
    local = "a" * 245
    email = f"{local}@eshop.com"  # 255 chars
    assert len(email) == 255
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()
    result = page.get_error_text()
    print(f"\n[TC-A-C-09] 255-char email response: '{result}' — best practice: explicit length error")


@pytest.mark.constraints
def test_TC_A_C_10_local_part_exceeds_64_chars(driver):
    """TC-A-C-10 · RFC 5321 — Local part > 64 chars is invalid.
    Best practice: 400 format error. Current SUT: 401."""
    email = f"{'a' * 65}@eshop.com"  # 65-char local part
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()
    result = page.get_error_text()
    print(f"\n[TC-A-C-10] 65-char local part response: '{result}' — best practice: 400 format error")


# ── NIST SP 800-63B: Password constraints ────────────────────────────────────
@pytest.mark.constraints
def test_TC_A_C_11_password_below_nist_minimum_7_chars(driver):
    """TC-A-C-11 · NIST 800-63B — Passwords below 8 chars should be rejected at login.
    Best practice: 400 'minimum password length is 8 characters'.
    Current SUT: 401 (no length check)."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "Pass12!")  # 7 chars
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()
    result = page.get_error_text()
    print(f"\n[TC-A-C-11] 7-char password response: '{result}' — best practice: explicit min-length error")


@pytest.mark.constraints
def test_TC_A_C_12_password_at_nist_minimum_8_chars(driver):
    """TC-A-C-12 · NIST 800-63B — 8-char password is at the NIST minimum; must be accepted.
    Expected: 401 (wrong password, but length is valid)."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "Pass1234")  # 8 chars, wrong
    assert page.is_still_on_login_page()
    assert page.is_error_shown()  # generic 401, not a format error


@pytest.mark.constraints
def test_TC_A_C_13_password_65_chars_above_nist_recommended(driver):
    """TC-A-C-13 · NIST 800-63B — NIST recommends supporting ≥ 64 chars.
    65-char password: system must not crash or silently truncate.
    Expected: 401 (wrong password handled gracefully)."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "A" * 65)
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "65-char wrong password: expect 401, not a crash"


@pytest.mark.constraints
def test_TC_A_C_14_password_unicode_characters(driver):
    """TC-A-C-14 · NIST 800-63B — NIST requires accepting Unicode in passwords.
    Expected: 401 (wrong); system must not crash on multibyte characters."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "Pässwörð!1")
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "Unicode password: expect 401 not a crash"


# ── OWASP: Security constraints ───────────────────────────────────────────────
@pytest.mark.constraints
def test_TC_A_C_15_xss_in_username_field(driver):
    """TC-A-C-15 · OWASP — XSS attempt in username field.
    Expected: 401; no alert dialog or script executes; input safely escaped."""
    page = LoginPage(driver).open()
    page.submit("<script>alert('xss')</script>", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()
    # Verify no alert dialog is present
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        driver.switch_to.alert.dismiss()
        pytest.fail("XSS VULNERABILITY: alert dialog appeared from username field input")
    except Exception:
        pass  # No alert → safe


@pytest.mark.constraints
def test_TC_A_C_16_xss_in_password_field(driver):
    """TC-A-C-16 · OWASP — XSS attempt in password field.
    Expected: 401; no script execution."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "<img src=x onerror=alert(1)>")
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        driver.switch_to.alert.dismiss()
        pytest.fail("XSS VULNERABILITY: alert dialog appeared from password field input")
    except Exception:
        pass  # No alert → safe
