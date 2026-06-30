"""
conftest.py — shared fixtures and database helpers for FR-02 login tests.

SUT:  EShop frontend-web  → http://localhost:5173
      EShop backend API   → http://localhost:3000
DB:   eshop-sut/backend/database.sqlite (SQLite, direct access for state setup)
"""
import os
import sqlite3
import time
from datetime import datetime, timedelta, timezone

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_URL = "http://localhost:5173"
TEST_EMAIL = "test@eshop.com"
TEST_PASSWORD = "Test1234!"

# Resolve the SQLite DB path relative to this file:
# selenium/ → artifacts/ → week_2/ → hw-group-06/ → testing/ → eshop-sut/
_HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.normpath(
    os.path.join(_HERE, "../../../../eshop-sut/backend/database.sqlite")
)


# ── Database helpers ───────────────────────────────────────────────────────────
def _connect() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"SQLite database not found at: {DB_PATH}\n"
            "Run `node database.js` inside eshop-sut/backend/ first."
        )
    return sqlite3.connect(DB_PATH)


def db_reset_account(email: str = TEST_EMAIL) -> None:
    """Reset login_attempts=0 and locked_until=NULL for the test account."""
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET login_attempts = 0, locked_until = NULL WHERE email = ?",
            (email,),
        )


def db_set_attempts(attempts: int, email: str = TEST_EMAIL) -> None:
    """Directly set the login_attempts counter (for BVA pre-conditions)."""
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET login_attempts = ? WHERE email = ?",
            (attempts, email),
        )


def db_lock_account(minutes: float = 3, email: str = TEST_EMAIL) -> None:
    """Set locked_until = now + minutes (simulate a fresh lockout)."""
    locked_until = (
        datetime.now(timezone.utc) + timedelta(minutes=minutes)
    ).isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET locked_until = ? WHERE email = ?",
            (locked_until, email),
        )


def db_set_lock_expired(seconds_ago: float = 60, email: str = TEST_EMAIL) -> None:
    """Set locked_until to a past timestamp (simulate an expired lock)."""
    locked_until = (
        datetime.now(timezone.utc) - timedelta(seconds=seconds_ago)
    ).isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET locked_until = ? WHERE email = ?",
            (locked_until, email),
        )


def db_set_lock_expiring_in(seconds: float, email: str = TEST_EMAIL) -> None:
    """Set locked_until to expire in exactly `seconds` from now."""
    locked_until = (
        datetime.now(timezone.utc) + timedelta(seconds=seconds)
    ).isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET locked_until = ? WHERE email = ?",
            (locked_until, email),
        )


# ── Selenium fixtures ──────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """Provide a fresh Chrome WebDriver instance per test function."""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless=new")  # Uncomment for CI / headless mode
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)
    drv.set_page_load_timeout(15)
    yield drv
    drv.quit()


@pytest.fixture()
def clean_account():
    """Reset the test account to clean state before and after each test."""
    db_reset_account()
    yield
    db_reset_account()


@pytest.fixture()
def one_failure_account():
    """Account with exactly 1 failed attempt (login_attempts=2 due to +2 bug)."""
    db_reset_account()
    db_set_attempts(2)
    yield
    db_reset_account()


@pytest.fixture()
def locked_account():
    """Account actively locked for 3 minutes."""
    db_reset_account()
    db_lock_account(minutes=3)
    yield
    db_reset_account()


@pytest.fixture()
def expired_lock_account():
    """Account whose lock expired 60 seconds ago."""
    db_set_lock_expired(seconds_ago=60)
    yield
    db_reset_account()


# ── Feature B (Shopping Cart) helpers ─────────────────────────────────────────
import requests as _requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

API_URL = "http://localhost:3000"


def get_api_token(email: str = TEST_EMAIL, password: str = TEST_PASSWORD) -> str:
    """Get a JWT token from the backend API (fast, avoids UI login flow)."""
    resp = _requests.post(
        f"{API_URL}/api/login",
        json={"email": email, "password": password},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def inject_auth_token(driver, token: str) -> None:
    """Store a JWT in localStorage then reload so AuthContext picks it up."""
    driver.execute_script(f"localStorage.setItem('token', '{token}')")
    driver.refresh()


def db_delete_test_orders(user_email: str = TEST_EMAIL) -> None:
    """Delete all orders created by the test user — call before/after checkout tests."""
    with _connect() as conn:
        conn.execute(
            "DELETE FROM orders WHERE user_id = (SELECT id FROM users WHERE email = ?)",
            (user_email,),
        )


def db_get_last_order(user_email: str = TEST_EMAIL):
    """Return the most recent order row for the test user, or None."""
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT o.id, o.total_amount, o.status, o.shipping_address
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE u.email = ?
            ORDER BY o.id DESC LIMIT 1
            """,
            (user_email,),
        ).fetchone()
    if row is None:
        return None
    return {
        "id": row[0],
        "total_amount": row[1],
        "status": row[2],
        "shipping_address": row[3],
    }


def click_cart_nav(driver, timeout: int = 8) -> None:
    """Click the 'Giỏ hàng' nav link (React Router — preserves client-side cart state)."""
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Giỏ hàng']"))
    ).click()


def click_checkout_btn(driver, timeout: int = 8) -> None:
    """Click the 'Tiến hành thanh toán' button on the cart page; accept alert if shown."""
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Tiến hành thanh toán')]")
        )
    ).click()
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass  # No alert — user is authenticated


@pytest.fixture()
def logged_in_driver(driver):
    """Chrome driver with the test user authenticated via localStorage token injection.

    After this fixture:
    - Driver is at BASE_URL (home page)
    - 'Thoát' button is visible in the header
    - Cart is empty (fresh React state after reload)
    """
    db_reset_account()
    token = get_api_token()
    driver.get(BASE_URL)
    inject_auth_token(driver, token)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Thoát']"))
    )
    return driver


@pytest.fixture()
def clean_orders():
    """Delete test-user orders before and after each test that runs through checkout."""
    db_delete_test_orders()
    yield
    db_delete_test_orders()


# ── Feature C (Coupon Management) helpers ─────────────────────────────────────

ADMIN_URL   = "http://localhost:5174"
ADMIN_EMAIL = "admin@eshop.com"
ADMIN_PASSWORD = "Admin123!"


def db_create_coupon(
    code: str,
    type_: str = "fixed",
    discount_value: int = 10000,
    min_order_amount: int = 0,
    expired_at: str = "2099-12-31",
    max_uses_per_user: int = 1,
    is_active: int = 1,
) -> int:
    """Insert a coupon directly into the DB; returns the new coupon id."""
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO coupons
               (code, type, discount_value, min_order_amount, expired_at,
                is_active, max_uses_per_user)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (code, type_, discount_value, min_order_amount, expired_at,
             is_active, max_uses_per_user),
        )
        return cur.lastrowid


def db_delete_coupon_by_code(*codes: str) -> None:
    """Delete coupons by code (accepts multiple codes)."""
    with _connect() as conn:
        for code in codes:
            conn.execute("DELETE FROM coupons WHERE code = ?", (code,))


def db_get_coupon_by_code(code: str):
    """Return the coupon row as a dict, or None if not found."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, code, type, discount_value, min_order_amount, "
            "expired_at, is_active, max_uses_per_user FROM coupons WHERE code = ?",
            (code,),
        ).fetchone()
    if row is None:
        return None
    keys = ["id", "code", "type", "discount_value", "min_order_amount",
            "expired_at", "is_active", "max_uses_per_user"]
    return dict(zip(keys, row))


def inject_admin_token(driver, token: str) -> None:
    """Store a JWT as 'adminToken' in localStorage so the admin panel picks it up."""
    driver.execute_script(f"localStorage.setItem('adminToken', '{token}')")
    driver.refresh()


@pytest.fixture()
def admin_driver(driver):
    """Chrome driver authenticated on the admin panel at ADMIN_URL.

    After this fixture:
    - Driver is at ADMIN_URL with admin logged in
    - Sidebar is visible; no specific tab is active
    """
    token = get_api_token(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
    driver.get(ADMIN_URL)
    inject_admin_token(driver, token)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(text(),'Mã Giảm Giá')]")
        )
    )
    return driver
