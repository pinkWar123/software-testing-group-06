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
