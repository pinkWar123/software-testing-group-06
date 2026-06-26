"""
tests/test_login_bva.py
FR-02: Login and Account Lockout — Boundary Value Analysis (TC-A-BV-01 → TC-A-BV-22)

Technique : Boundary Value Analysis (ISTQB black-box)
Boundaries: failed-attempt threshold · lock duration · username length ·
            username local-part length · password length (NIST SP 800-63B)
"""
import time
import pytest

from conftest import (
    TEST_EMAIL, TEST_PASSWORD,
    db_reset_account, db_set_attempts, db_lock_account,
    db_set_lock_expired, db_set_lock_expiring_in,
)
from pages.login_page import LoginPage


@pytest.fixture(autouse=True)
def _reset(driver):
    db_reset_account()
    yield
    db_reset_account()


# ── Boundary 1: Failed attempts vs lockout threshold ──────────────────────────
@pytest.mark.bva
def test_TC_A_BV_01_first_wrong_attempt_no_lock(driver):
    """TC-A-BV-01 — In point (0 failures → 1st wrong attempt): account stays open."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "WrongPass99")
    assert page.is_still_on_login_page()
    # Still able to submit again → not locked
    page.open().submit(TEST_EMAIL, "WrongPass99")
    assert page.is_still_on_login_page()


@pytest.mark.bva
def test_TC_A_BV_02_one_failure_just_below_threshold(driver):
    """TC-A-BV-02 — Off point (1 failure state): account still open, can retry.
    With +2 bug: login_attempts=2 after first failure; 2 < threshold of 3 → not locked."""
    db_set_attempts(2)  # state after 1st wrong attempt
    page = LoginPage(driver).open()
    # Entering the correct password should succeed (not yet locked)
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), (
        "Account with 1 failure (login_attempts=2) should NOT be locked yet"
    )


@pytest.mark.bva
def test_TC_A_BV_03_second_wrong_attempt_triggers_lock(driver):
    """TC-A-BV-03 — On point: 2nd consecutive wrong attempt → lockout triggered.
    With +2 bug: 0→2 after attempt 1 (not locked), 2→4 after attempt 2 (locked)."""
    db_set_attempts(2)  # 1 prior failure
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "WrongPass99")
    # Next attempt with correct password must also fail (account now locked)
    page.open().submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "Account should be locked after 2nd wrong attempt"


@pytest.mark.bva
def test_TC_A_BV_04_correct_password_while_locked(driver):
    """TC-A-BV-04 — Out point: correct credentials during active lock → error."""
    db_lock_account(minutes=3)
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "Correct credentials must be rejected while account is locked"


# ── Boundary 2: Lock duration (≈180 seconds) ─────────────────────────────────
@pytest.mark.bva
@pytest.mark.slow
def test_TC_A_BV_05_locked_at_60s_still_locked(driver):
    """TC-A-BV-05 — In point (~60 s into 3-min lock): still locked."""
    db_lock_account(minutes=3)
    time.sleep(2)  # just a small wait; ~177 s remain
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.bva
@pytest.mark.slow
def test_TC_A_BV_06_locked_at_179s_still_locked(driver):
    """TC-A-BV-06 — Off point (1 s before expiry): must still be locked.
    Sets locked_until = now + 3s then waits 2s → 1s remaining."""
    db_set_lock_expiring_in(seconds=3)
    time.sleep(2)  # 1 s remaining
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_still_on_login_page(), "Account should still be locked 1 s before expiry"


@pytest.mark.bva
@pytest.mark.slow
def test_TC_A_BV_07_login_at_expiry_boundary(driver):
    """TC-A-BV-07 — On point (at expiry ≈180 s): documents > vs >= boundary.
    Sets locked_until = now + 3s, waits 4s → lock should be expired."""
    db_set_lock_expiring_in(seconds=3)
    time.sleep(4)  # lock_until is now in the past by ~1s
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    # Document observed boundary behaviour
    if page.is_login_successful():
        print("\n[TC-A-BV-07] Boundary: lock expired → login succeeds (condition: locked_until > now)")
    else:
        print("\n[TC-A-BV-07] Boundary: login still blocked at expiry moment (condition: locked_until >= now)")


@pytest.mark.bva
@pytest.mark.slow
def test_TC_A_BV_08_login_after_lock_expires(driver):
    """TC-A-BV-08 — Out point (1 s after expiry): lock expired, login succeeds."""
    db_set_lock_expired(seconds_ago=5)  # lock expired 5 s ago
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), "Login must succeed once lock has expired"


# ── Boundary 3: Username string length ───────────────────────────────────────
@pytest.mark.bva
def test_TC_A_BV_09_username_empty_off_point(driver):
    """TC-A-BV-09 — Off point (0 chars): HTML5 required blocks submission."""
    page = LoginPage(driver).open()
    page.enter_password(TEST_PASSWORD).click_sign_in()
    assert page.is_still_on_login_page()


@pytest.mark.bva
def test_TC_A_BV_10_username_one_char_on_point(driver):
    """TC-A-BV-10 — On point (1 char): minimum non-empty → 401 (not registered)."""
    page = LoginPage(driver).open()
    page.submit("a", TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


# ── Boundary 4: Password string length ───────────────────────────────────────
@pytest.mark.bva
def test_TC_A_BV_11_password_empty_off_point(driver):
    """TC-A-BV-11 — Off point (0 chars): HTML5 required blocks submission."""
    page = LoginPage(driver).open()
    page.enter_username(TEST_EMAIL).click_sign_in()
    assert page.is_still_on_login_page()


@pytest.mark.bva
def test_TC_A_BV_12_password_one_char_on_point(driver):
    """TC-A-BV-12 — On point (1 char wrong password): 401, counter incremented."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "X")
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


# ── Boundary 5: Lockout counter reset ────────────────────────────────────────
@pytest.mark.bva
def test_TC_A_BV_13_counter_resets_after_successful_login(driver):
    """TC-A-BV-13 — Counter reset boundary: login success resets attempts to 0.
    After reset, the next wrong attempt should behave as attempt #1 (not #2)."""
    db_set_attempts(2)  # 1 prior failure
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), "Should succeed with correct password"
    # Now do 1 wrong attempt from the reset state — should NOT lock
    page.open().submit(TEST_EMAIL, "WrongPass99")
    page.open().submit(TEST_EMAIL, TEST_PASSWORD)
    assert page.is_login_successful(), "After reset, 1 wrong attempt should not lock account"


# ── Boundary 6: Username total length (RFC 5321 max = 254 chars) ─────────────
@pytest.mark.bva
def test_TC_A_BV_14_username_253_chars_below_rfc_max(driver):
    """TC-A-BV-14 — Off point below RFC max (253 chars): valid length → 401 not registered."""
    # 253 chars = 241 'a' chars + '@' + 'eshop.com' (9 chars) = 251 → pad to 253
    local = "a" * 243
    email = f"{local}@eshop.com"  # 243 + 1 + 9 = 253 chars
    assert len(email) == 253
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.bva
def test_TC_A_BV_15_username_254_chars_at_rfc_max(driver):
    """TC-A-BV-15 — On point at RFC max (254 chars): system should accept length → 401."""
    local = "a" * 244
    email = f"{local}@eshop.com"  # 244 + 1 + 9 = 254 chars
    assert len(email) == 254
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "254-char email is RFC-valid; should get 401 not a format error"


@pytest.mark.bva
def test_TC_A_BV_16_username_255_chars_exceeds_rfc_max(driver):
    """TC-A-BV-16 — Out point above RFC max (255 chars).
    Best practice: server should reject with 400/413.
    Observed: server likely returns 401 (no length check)."""
    local = "a" * 245
    email = f"{local}@eshop.com"  # 245 + 1 + 9 = 255 chars
    assert len(email) == 255
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    result = "rejected (400/form error)" if page.is_error_shown() else "accepted (no length check)"
    print(f"\n[TC-A-BV-16] 255-char username: {result} — best practice: should be rejected")
    assert page.is_still_on_login_page()


# ── Boundary 7: Username local-part length (RFC 5321 max = 64) ───────────────
@pytest.mark.bva
def test_TC_A_BV_17_local_part_64_chars_at_rfc_max(driver):
    """TC-A-BV-17 — On point (64-char local part): valid per RFC → 401 not registered."""
    email = f"{'a' * 64}@eshop.com"
    assert email.index("@") == 64
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.bva
def test_TC_A_BV_18_local_part_65_chars_exceeds_rfc_max(driver):
    """TC-A-BV-18 — Out point (65-char local part): exceeds RFC 5321 max.
    Best practice: server should return 400. Observed: likely 401."""
    email = f"{'a' * 65}@eshop.com"
    page = LoginPage(driver).open()
    page.submit(email, TEST_PASSWORD)
    result = "error shown" if page.is_error_shown() else "no error (accepted silently)"
    print(f"\n[TC-A-BV-18] 65-char local part: {result} — best practice: 400 format error")
    assert page.is_still_on_login_page()


# ── Boundary 8: Password length (NIST SP 800-63B) ────────────────────────────
@pytest.mark.bva
def test_TC_A_BV_19_password_7_chars_below_nist_min(driver):
    """TC-A-BV-19 — Off point (7 chars, below NIST min of 8).
    Best practice: reject with 'password too short'. Observed: likely 401 (no check)."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "Pass12!")  # 7 chars
    assert page.is_still_on_login_page()
    result = "format-error shown" if "quá ngắn" in page.get_error_text().lower() else "generic 401"
    print(f"\n[TC-A-BV-19] 7-char password: {result} — best practice: explicit min-length error")


@pytest.mark.bva
def test_TC_A_BV_20_password_8_chars_at_nist_min(driver):
    """TC-A-BV-20 — On point (8 chars, at NIST min): length valid → 401 wrong password."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "Pass1234")  # 8 chars, wrong password
    assert page.is_still_on_login_page()
    assert page.is_error_shown()


@pytest.mark.bva
def test_TC_A_BV_21_password_64_chars_nist_recommended_max(driver):
    """TC-A-BV-21 — On point (64 chars): NIST recommends supporting ≥ 64 → no crash."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "A" * 64)  # wrong 64-char password
    assert page.is_still_on_login_page()
    assert page.is_error_shown(), "64-char password should work without crash → 401"


@pytest.mark.bva
def test_TC_A_BV_22_password_65_chars_above_nist_max(driver):
    """TC-A-BV-22 — Out point (65 chars): NIST says don't truncate beyond 64.
    System must not crash or silently truncate; 401 expected."""
    page = LoginPage(driver).open()
    page.submit(TEST_EMAIL, "A" * 65)  # wrong 65-char password
    assert page.is_still_on_login_page()
    # Must not crash (timeout/500 would indicate truncation issue)
    assert page.is_error_shown(), "65-char password: system must handle gracefully → 401"
