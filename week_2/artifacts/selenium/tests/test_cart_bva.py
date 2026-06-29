"""
tests/test_cart_bva.py
FR-07: Shopping Cart — Boundary Value Analysis (TC-B-BV-01 → TC-B-BV-15)

BVA variables:
  - quantity via mobile normalizeQuantity  (BVA-01..05) → SKIP (mobile-only)
  - quantity server-side via /api/cart      (BVA-06..08) → SKIP (dead endpoint)
  - total_amount at checkout via web UI     (BVA-09..11) → TESTABLE
  - shipping_address length                 (BVA-12..15) → SKIP (API-only)
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import db_delete_test_orders
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(autouse=True)
def _cleanup_orders():
    db_delete_test_orders()
    yield
    db_delete_test_orders()


# ── TC-B-BV-01 to 05: SKIP (mobile normalizeQuantity — React Native / Appium) ─

@pytest.mark.skip(
    reason="TC-B-BV-01: Mobile-only. normalizeQuantity(-1): parseInt('-1')=-1, "
           "not >0 → normalised to 1. Requires Appium."
)
@pytest.mark.cart_bva
def test_TC_B_BV_01_mobile_qty_negative_normalised(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-02: Mobile-only. normalizeQuantity(0): parseInt('0')=0, "
           "not >0 → normalised to 1. Off-point. Requires Appium."
)
@pytest.mark.cart_bva
def test_TC_B_BV_02_mobile_qty_zero_normalised(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-03: Mobile-only. normalizeQuantity(1): on-point. "
           "parseInt('1')=1 >0 → accepted as 1. Requires Appium."
)
@pytest.mark.cart_bva
def test_TC_B_BV_03_mobile_qty_one_on_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-04: Mobile-only. float truncation: parseInt('1.5')=1 >0 → qty=1. "
           "Requires Appium."
)
@pytest.mark.cart_bva
def test_TC_B_BV_04_mobile_qty_float_truncation(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-05: Mobile-only. float below 1: parseInt('0.9')=0, not >0 → qty=1. "
           "Requires Appium."
)
@pytest.mark.cart_bva
def test_TC_B_BV_05_mobile_qty_float_below_one(driver):
    pass


# ── TC-B-BV-06 to 08: SKIP (server /api/cart — dead endpoint) ─────────────────

@pytest.mark.skip(
    reason="TC-B-BV-06: API-only. qty=1 on-point on dead /api/cart endpoint. "
           "Test via curl: POST /api/cart {quantity:1}."
)
@pytest.mark.cart_bva
def test_TC_B_BV_06_server_qty_one_on_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-07: API-only. qty=0 off-point on dead /api/cart endpoint "
           "(no server validation — confirms BUG-B-01). Test via curl."
)
@pytest.mark.cart_bva
def test_TC_B_BV_07_server_qty_zero_off_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-08: API-only. qty=999999 upper-extreme on dead /api/cart endpoint. "
           "Test via curl: POST /api/cart {quantity:999999}."
)
@pytest.mark.cart_bva
def test_TC_B_BV_08_server_qty_extreme_upper(driver):
    pass


# ── Shared helper: add product and go to checkout ─────────────────────────────

def _add_and_reach_checkout(logged_in_driver):
    """Helper: add first product from home, navigate to checkout."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)
    home.click_cart_nav()
    CartPage(logged_in_driver).wait_for_load().click_checkout()
    return CheckoutPage(logged_in_driver).wait_for_load()


# ── TC-B-BV-09: total_amount = 1 (on-point: minimum valid) ───────────────────

@pytest.mark.cart_bva
def test_TC_B_BV_09_checkout_total_one_on_point(logged_in_driver):
    """TC-B-BV-09 — Set checkout total to 1 (minimum positive value).
    Expected: server creates order (total=1 is valid per current logic — debatable
    minimum, but server has no lower-bound enforcement above 0).
    Documents that server accepts any positive total_amount."""
    checkout = _add_and_reach_checkout(logged_in_driver)
    checkout.set_total(1).confirm_order()
    assert checkout.is_success(), (
        "TC-B-BV-09: Server should accept total_amount=1 as on-point minimum. "
        "If this fails, server added a lower-bound check — update test."
    )


# ── TC-B-BV-10: total_amount = 0 (off-point — just below valid) ───────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-02: Server does not enforce total_amount > 0. "
           "Expected: 400 (reject zero). Actual: order accepted with total=0."
)
@pytest.mark.cart_bva
def test_TC_B_BV_10_checkout_total_zero_off_point_rejected(logged_in_driver):
    """TC-B-BV-10 — Set checkout total to 0 (off-point: just below minimum valid).
    CORRECT assertion: server REJECTS total=0. Currently XFAIL (BUG-B-02)."""
    checkout = _add_and_reach_checkout(logged_in_driver)
    checkout.set_total(0).confirm_order()
    assert not checkout.is_success(), (
        "BUG-B-02: Server accepted total=0 — should reject off-point zero total."
    )


# ── TC-B-BV-11: total_amount = -100 (out-point — negative) ──────────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-02: Server does not validate negative total_amount. "
           "Expected: 400 (reject). Actual: order accepted with total=-100."
)
@pytest.mark.cart_bva
def test_TC_B_BV_11_checkout_total_negative_out_point_rejected(logged_in_driver):
    """TC-B-BV-11 — Set checkout total to -100 (out-point: beyond minimum).
    CORRECT assertion: server REJECTS negative total. Currently XFAIL (BUG-B-02)."""
    checkout = _add_and_reach_checkout(logged_in_driver)
    checkout.set_total(-100).confirm_order()
    assert not checkout.is_success(), (
        "BUG-B-02: Server accepted total=-100 — should reject negative total."
    )


# ── TC-B-BV-12 to 15: SKIP (shipping_address — API-only, UI sends no address) ─

@pytest.mark.skip(
    reason="TC-B-BV-12: API-only. shipping_address off-point (empty string). "
           "UI checkout never sends this field (BUG-B-06). "
           "Test via: POST /api/checkout {shipping_address: ''}."
)
@pytest.mark.cart_bva
def test_TC_B_BV_12_api_shipping_empty_off_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-13: API-only. shipping_address on-point (1 char 'A'). "
           "UI never sends address (BUG-B-06). Test via curl."
)
@pytest.mark.cart_bva
def test_TC_B_BV_13_api_shipping_one_char_on_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-14: N/A. shipping_address typical in-point ('123 Le Loi'). "
           "UI checkout form has NO address field (BUG-B-06) — every UI order "
           "is stored with NULL address regardless."
)
@pytest.mark.cart_bva
def test_TC_B_BV_14_api_shipping_typical_in_point(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-BV-15: API-only. shipping_address upper-edge (501 chars). "
           "No server length cap defined. Test via curl."
)
@pytest.mark.cart_bva
def test_TC_B_BV_15_api_shipping_upper_edge(driver):
    pass
