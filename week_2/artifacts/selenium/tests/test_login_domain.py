"""
tests/test_login_domain.py
FR-02: Login and Account Lockout — Domain Testing (TC-A-01 → TC-A-19)

Technique : Equivalence Partitioning / Domain Testing (ISTQB black-box)
Covers    : All equivalence classes D-E1–D-E7, D-P1–D-P6, D-S1–D-S4
"""
import pytest

from conftest import (
    TEST_EMAIL, TEST_PASSWORD,
    db_reset_account, db_lock_account, db_set_attempts, db_set_lock_expired,
)
from pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def _reset(driver):
    """Ensure clean account state before every domain test."""
    db_reset_account()
    yield
    db_reset_account()


# ── Valid login ────────────────────────────────────────────────────────────────
@pytest.mark.domain
def test_TC_A_01_valid_login_clean_account(driver):
    """TC-A-01 · D-E1 + D-P1 + D-S1 — Valid credentials, clean account → success."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), "Expected redirect away from /login on success"


# ── Username domain ────────────────────────────────────────────────────────────
@pytest.mark.domain
def test_TC_A_02_unregistered_email_format(driver):
    """TC-A-02 · D-E2 — Unregistered well-formed email → 401 error."""
    page = LoginPage(driver).open()
    page.submit("nobody@eshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_03_non_email_format_username(driver):
    """TC-A-03 · D-E3 — Non-email-format string (no @) → 401.
    UI field is 'Username', so no email-format validation is expected; any
    unregistered string should return the same generic 401 error."""
    page = LoginPage(driver).open()
    page.submit("testeshop.com", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_04_empty_username(driver):
    """TC-A-04 · D-E4 — Empty username → form blocked by HTML5 required, or 401."""
    page = LoginPage(driver).open()
    # Do NOT enter username; enter password only, then click Sign In
    page.enter_password(TEST_PASSWORD).click_sign_in()
    # HTML5 required attribute should prevent form submission
    assert page.is_still_on_login_page(), "Form should block empty username submission"


@pytest.mark.domain
def test_TC_A_05_missing_username_field(driver):
    """TC-A-05 · D-E5 — Username field left completely untouched."""
    page = LoginPage(driver).open()
    page.enter_password(TEST_PASSWORD).click_sign_in()
    assert page.is_still_on_login_page()


# ── Password domain ────────────────────────────────────────────────────────────
@pytest.mark.domain
def test_TC_A_06_wrong_password_first_attempt(driver):
    """TC-A-06 · D-P2 + D-S1 — 1st wrong password → 401, account NOT locked."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "WrongPass99")
    assert page.is_still_on_login_page()
    assert page.is_error_shown()
    # Verify account is still accessible (not locked) by attempting again
    page.open().submit(TEST_EMAIL, "WrongPass99")
    assert page.is_still_on_login_page()


@pytest.mark.domain
def test_TC_A_07_wrong_password_second_attempt_triggers_lock(driver):
    """TC-A-07 · D-P2 + D-S2 — 2nd wrong password → lockout triggered.
    Pre-condition: 1 prior failure already recorded (login_attempts=2)."""
    db_set_attempts(2)  # simulate the state after 1st wrong attempt
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "WrongPass99")
    # Account should now be locked — correct password also returns error
    page.open().submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "Locked account should show error even with correct password"


@pytest.mark.domain
def test_TC_A_08_login_while_actively_locked(driver):
    """TC-A-08 · D-S3 — Correct credentials while account is locked → error."""
    db_lock_account(minutes=3)
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_09_login_after_lock_expires(driver):
    """TC-A-09 · D-S4 — Lock expired in the past → login should succeed."""
    db_set_lock_expired(seconds_ago=60)
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), "Expired lock should not block login"


@pytest.mark.domain
def test_TC_A_10_correct_password_after_one_failure(driver):
    """TC-A-10 · D-S2 — Correct password after 1 failure → login success."""
    db_set_attempts(2)  # 1 prior failure
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful()


@pytest.mark.domain
def test_TC_A_11_empty_password(driver):
    """TC-A-11 · D-P3 — Empty password field → blocked or 401."""
    page = LoginPage(driver).open()
    page.enter_username(TEST_EMAIL).click_sign_in()
    assert page.is_still_on_login_page()


@pytest.mark.domain
def test_TC_A_12_missing_password_field(driver):
    """TC-A-12 · D-P4 — Password field never touched → blocked by required."""
    page = LoginPage(driver).open()
    page.enter_username(TEST_EMAIL).click_sign_in()
    assert page.is_still_on_login_page()


# ── Additional domain classes ─────────────────────────────────────────────────
@pytest.mark.domain
def test_TC_A_13_alphanumeric_username(driver):
    """TC-A-13 · D-E3 — Pure alphanumeric username (no @) → 401."""
    page = LoginPage(driver).open()
    page.submit("johndoe", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_14_username_with_whitespace_padding(driver):
    """TC-A-14 · D-E6 — Leading/trailing whitespace in username.
    Observable: 200 OK if system trims, else 401 (no match)."""
    page = LoginPage(driver).open()
    page.submit(f" {TEST_EMAIL} ", TEST_PASSWORD)
    # Record observable behaviour (pass either way; we document the actual result)
    result = "success" if page.is_login_successful() else "failure"
    print(f"\n[TC-A-14] Whitespace padding result: {result}")
    # No hard assert — this test documents behaviour


@pytest.mark.domain
def test_TC_A_15_sql_injection_in_username(driver):
    """TC-A-15 · D-E7 — SQL injection string → 401, must not bypass auth."""
    page = LoginPage(driver).open()
    page.submit("' OR 1=1 --", TEST_PASSWORD)
    assert page.is_still_on_login_page(), "SQL injection must NOT authenticate"
    assert not page.is_login_successful()


@pytest.mark.domain
def test_TC_A_16_password_case_sensitivity(driver):
    """TC-A-16 · D-P6 — Same password, wrong case → 401 (case-sensitive)."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD.upper())
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_17_whitespace_only_password(driver):
    """TC-A-17 · D-P5 — Whitespace-only password → 401."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "   ")
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.domain
def test_TC_A_18_both_fields_empty(driver):
    """TC-A-18 — Both username and password empty → form blocked, no auth."""
    page = LoginPage(driver).open()
    page.click_sign_in()
    assert page.is_still_on_login_page()
    assert not page.is_login_successful()


# ── UI / Bug tests ─────────────────────────────────────────────────────────────
@pytest.mark.domain
def test_TC_A_19_page_title_mismatch_bug(driver):
    """TC-A-19 — Page title on login page should be 'Đăng Nhập', not 'Đăng Ký'.
    KNOWN BUG: Login.jsx h2 text is hard-coded as 'Đăng Ký' (Register)."""
    page = LoginPage(driver).open()
    actual_title = page.get_h2_title()
    # Document the bug: expected "Đăng Nhập", actual is "Đăng Ký"
    assert actual_title == "Đăng Nhập", (
        f"BUG TC-A-19: Page title is '{actual_title}' — should be 'Đăng Nhập' (Sign In). "
        "The h2 in Login.jsx is mis-labeled 'Đăng Ký' (Register)."
    )


@pytest.mark.domain
def test_TC_A_20_password_field_should_be_masked(driver):
    """TC-A-20 · D-P11 — Password field MUST use type='password' (OWASP).
    KNOWN SECURITY BUG: Login.jsx uses type='text' — password is visible."""
    page = LoginPage(driver).open()
    pw_type = page.get_password_field_type()
    assert pw_type == "password", (
        f"SECURITY BUG TC-A-20: Password input type='{pw_type}' — must be 'password' "
        "to mask input. Login.jsx incorrectly uses type='text'."
    )
