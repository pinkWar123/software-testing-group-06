"""
tests/test_cart_domain.py
FR-07: Shopping Cart — Domain Testing (TC-B-01 → TC-B-29 + OWASP constraints)

Scope   : Web frontend (localhost:5173) + backend (localhost:3000)
Platform: Selenium 4 + pytest

Test classification:
  PASS   — test asserts correct / current behaviour; expected to succeed
  XFAIL  — test asserts the CORRECT expectation; currently fails due to a documented bug
  SKIP   — cannot be verified via Selenium: API-only (dead endpoint) or mobile-only

Important architecture facts (verified from source):
  - Cart is CLIENT-SIDE React state (CartContext.useState).
    /GET /POST /api/cart are orphaned dead code — no frontend calls them.
  - Cart state resets on any full page reload (driver.get()).
    Use header 'Giỏ hàng' link (React Router) to preserve cart state.
  - Only /api/checkout is called from the UI.
  - Web Checkout.jsx renders total_amount as an EDITABLE <input type='number'>.
  - No shipping_address field exists in the checkout UI form.
"""
import math

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import (
    BASE_URL, TEST_EMAIL, TEST_PASSWORD,
    db_delete_test_orders, db_get_last_order, db_reset_account,
    get_api_token,
)
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# ── Module-level order cleanup (runs before and after every test) ──────────────
@pytest.fixture(autouse=True)
def _cleanup_orders():
    db_delete_test_orders()
    yield
    db_delete_test_orders()


# ── TC-B-01 to TC-B-06: SKIP (orphaned /api/cart endpoint — no UI caller) ─────

@pytest.mark.skip(
    reason="TC-B-01: API-only — POST /api/cart is orphaned dead code (no frontend calls it). "
           "Verified: grep shows zero /api/cart references in any frontend. "
           "Test via curl: POST http://localhost:3000/api/cart with valid body."
)
@pytest.mark.cart_domain
def test_TC_B_01_api_cart_valid_quantity(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-02: API-only — same as TC-B-01. Min-valid quantity boundary (qty=1) "
           "on the dead /api/cart endpoint."
)
@pytest.mark.cart_domain
def test_TC_B_02_api_cart_qty_min_valid(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-03: API-only — qty=0 accepted by dead /api/cart endpoint (no validation). "
           "Reveals BUG-B-01. Test via curl."
)
@pytest.mark.cart_domain
def test_TC_B_03_api_cart_qty_zero_bug(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-04: API-only — qty=-1 accepted by dead /api/cart endpoint (no validation). "
           "Reveals BUG-B-01. Test via curl."
)
@pytest.mark.cart_domain
def test_TC_B_04_api_cart_qty_negative_bug(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-05: Mobile-only — normalizeQuantity('abc') on React Native. "
           "Requires Appium/physical device. Expected: qty normalised to 1."
)
@pytest.mark.cart_domain
def test_TC_B_05_mobile_nonnumeric_qty(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-06: Mobile-only — normalizeQuantity('1.5') on React Native. "
           "parseInt('1.5')=1 → qty=1. Requires Appium."
)
@pytest.mark.cart_domain
def test_TC_B_06_mobile_float_qty(driver):
    pass


# ── TC-B-07: Checkout with valid total ────────────────────────────────────────

@pytest.mark.cart_domain
def test_TC_B_07_checkout_valid_total(logged_in_driver):
    """TC-B-07 — Add product from home (qty=1), checkout without altering total.
    Expected: 200 OK, order created, success screen shown."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)
    home.click_cart_nav()

    cart = CartPage(logged_in_driver).wait_for_load()
    assert cart.get_row_count() == 1, "Cart should have 1 item before checkout"
    cart.click_checkout()

    checkout = CheckoutPage(logged_in_driver).wait_for_load()
    initial_total = checkout.get_total_value()
    assert initial_total and initial_total != "0", (
        f"Checkout total should reflect cart (got '{initial_total}')"
    )
    checkout.confirm_order()
    assert checkout.is_success(), "Order should succeed with valid positive total"


# ── TC-B-08: Checkout total=0 (BUG-B-02 — server accepts anything) ───────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-02: Server does not validate total_amount. Expected: reject total=0 "
           "(400). Actual: order created with total=0 (server.js:299-308 — no check)."
)
@pytest.mark.cart_domain
def test_TC_B_08_checkout_total_zero_rejected(logged_in_driver):
    """TC-B-08 — Set checkout total to 0. CORRECT expectation: server rejects.
    Currently XFAIL: server accepts it (BUG-B-02)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)
    home.click_cart_nav()
    CartPage(logged_in_driver).wait_for_load().click_checkout()

    checkout = CheckoutPage(logged_in_driver).wait_for_load()
    checkout.set_total(0).confirm_order()
    # CORRECT assertion: should NOT succeed. Will XFAIL until bug is fixed.
    assert not checkout.is_success(), "Server should reject total_amount=0"


# ── TC-B-09: Checkout total=-1 (BUG-B-02) ────────────────────────────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-02: Server does not validate total_amount. Expected: reject negative. "
           "Actual: order accepted with total=-1."
)
@pytest.mark.cart_domain
def test_TC_B_09_checkout_total_negative_rejected(logged_in_driver):
    """TC-B-09 — Set checkout total to -1. CORRECT expectation: server rejects.
    Currently XFAIL: server accepts it (BUG-B-02)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)
    home.click_cart_nav()
    CartPage(logged_in_driver).wait_for_load().click_checkout()

    checkout = CheckoutPage(logged_in_driver).wait_for_load()
    checkout.set_total(-1).confirm_order()
    assert not checkout.is_success(), "Server should reject total_amount=-1"


# ── TC-B-10, B-11: SKIP (API-only) ───────────────────────────────────────────

@pytest.mark.skip(
    reason="TC-B-10: API-only — empty shipping_address not testable via UI because "
           "the web checkout form has NO shipping_address field (BUG-B-06). "
           "Test via: POST /api/checkout with {shipping_address: ''}."
)
@pytest.mark.cart_domain
def test_TC_B_10_api_checkout_empty_shipping(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-11: API-only price-manipulation bypass. The UI equivalent is TC-B-23 "
           "(editable checkout total). Test via curl: POST /api/checkout with "
           "{total_amount: 1} while cart has items worth 500,000."
)
@pytest.mark.cart_domain
def test_TC_B_11_api_total_bypass(driver):
    pass


# ── TC-B-12: Duplicate product on web (CartContext appends — BUG-B-04) ────────

@pytest.mark.cart_domain
def test_TC_B_12_web_duplicate_product_creates_two_entries(logged_in_driver):
    """TC-B-12 — Add the same product twice from home page.
    Web CartContext.addToCart appends (does NOT merge) → 2 separate entries.
    Mobile addToCart merges → 1 entry with summed qty. Documents BUG-B-04."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)  # first add
    home.add_product_to_cart(0)  # second add
    home.click_cart_nav()

    cart = CartPage(logged_in_driver).wait_for_load()
    row_count = cart.get_row_count()
    # DOCUMENT BUG-B-04: web creates TWO entries instead of merging
    assert row_count == 2, (
        f"BUG-B-04: Web CartContext appends duplicates — expected 2 entries, got {row_count}. "
        "CartContext.addToCart (CartContext.jsx:8-10) never checks for existing product id."
    )


# ── TC-B-13: Empty cart message ───────────────────────────────────────────────

@pytest.mark.cart_domain
def test_TC_B_13_empty_cart_shows_message(driver):
    """TC-B-13 — Navigate to /cart without adding any item.
    Expected: 'Giỏ hàng của bạn đang trống' message shown."""
    cart = CartPage(driver).open()
    assert cart.is_empty(), "Empty cart should show 'đang trống' message"
    assert cart.get_row_count() == 0, "No table rows should be present"


# ── TC-B-14: Add to cart without authentication (corrected expectation) ────────

@pytest.mark.cart_domain
def test_TC_B_14_add_to_cart_without_auth_succeeds(driver):
    """TC-B-14 — Add product from home without logging in.
    CORRECTED expected: ADD succeeds (cart is client-side React state, no auth needed).
    Original report had '401 Unauthorized' which was WRONG for the web UI.
    Auth is only required at checkout (Cart.jsx:11-17)."""
    home = HomePage(driver).open()
    home.add_product_to_cart(0)  # single click on home page — no auth needed
    home.click_cart_nav()

    cart = CartPage(driver).wait_for_load()
    assert not cart.is_empty(), (
        "Add-to-cart should succeed without auth (cart is client-side React state). "
        "Auth is enforced only at checkout."
    )
    assert cart.get_row_count() == 1


# ── TC-B-15: Checkout without authentication ─────────────────────────────────

@pytest.mark.cart_domain
def test_TC_B_15_checkout_without_auth_redirects_to_login(driver):
    """TC-B-15 — Add product (no auth), attempt checkout.
    Expected: alert shown, redirect to /login (Cart.jsx:11-17 guard)."""
    home = HomePage(driver).open()
    home.add_product_to_cart(0)
    home.click_cart_nav()

    cart = CartPage(driver).wait_for_load()
    cart.click_checkout()  # alert auto-accepted by click_checkout()

    WebDriverWait(driver, 6).until(
        lambda d: "/login" in d.current_url
    )
    assert "/login" in driver.current_url, (
        "Checkout without auth should redirect to /login"
    )


# ── TC-B-16: Checkout with empty cart (BUG) ───────────────────────────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG: Server should reject checkout with empty cart. "
           "Actual: server accepts it (total=0, empty items array)."
)
@pytest.mark.cart_domain
def test_TC_B_16_checkout_empty_cart_rejected(logged_in_driver):
    """TC-B-16 — Navigate directly to /checkout with empty cart (full reload).
    CORRECT expectation: server/UI rejects empty-cart checkout.
    Currently XFAIL: server creates order with total=0."""
    # Full page reload → cart empty, auth token kept from localStorage
    checkout = CheckoutPage(logged_in_driver).open()
    assert checkout.get_item_count() == 0, "Item list should be empty"
    total_val = checkout.get_total_value()
    assert total_val == "0", f"Total should be 0 for empty cart, got '{total_val}'"

    checkout.confirm_order()
    # CORRECT: should NOT succeed. Will XFAIL until bug is fixed.
    assert not checkout.is_success(), "Empty-cart checkout should be rejected"


# ── TC-B-17 to B-19: SKIP (API-only) ─────────────────────────────────────────

@pytest.mark.skip(
    reason="TC-B-17: API-only — null shipping_address not testable via UI (form has no field). "
           "Test via: POST /api/checkout {shipping_address: null}."
)
@pytest.mark.cart_domain
def test_TC_B_17_api_checkout_null_shipping(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-18: API-only — price=0 via dead POST /api/cart endpoint. "
           "Reveals BUG-B-05 (server accepts client-supplied price). Test via curl."
)
@pytest.mark.cart_domain
def test_TC_B_18_api_cart_zero_price(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-19: API-only — negative price via dead POST /api/cart endpoint. "
           "Reveals BUG-B-05. Test via curl."
)
@pytest.mark.cart_domain
def test_TC_B_19_api_cart_negative_price(driver):
    pass


# ── TC-B-20: Cart total calculation accuracy ─────────────────────────────────

@pytest.mark.cart_domain
def test_TC_B_20_cart_total_accuracy(logged_in_driver):
    """TC-B-20 — Add one product from home; verify cart total = price × qty.
    Expected: total = product_price × 1 (home-page addToCart always uses qty=1)."""
    home = HomePage(logged_in_driver).wait_for_products()
    price_text = home.get_first_product_price_text()
    home.add_product_to_cart(0)
    home.click_cart_nav()

    cart = CartPage(logged_in_driver).wait_for_load()
    assert cart.get_row_count() == 1

    # Quantity shown in cart should be 1 (home-page addToCart hardcodes qty=1)
    qty_text = cart.get_item_quantity_text(0)
    assert qty_text == "1", f"Expected qty=1 from home-page add, got '{qty_text}'"

    total_text = cart.get_cart_total_text()
    total_val   = CartPage.parse_vnd(total_text)
    price_val   = CartPage.parse_vnd(price_text.replace("VND", ""))

    assert not math.isnan(total_val), f"Cart total is NaN — parsing failed on: '{total_text}'"
    assert not math.isnan(price_val), f"Product price is NaN — parsing failed on: '{price_text}'"
    assert total_val == price_val * 1, (
        f"Cart total {total_val} ≠ price {price_val} × 1"
    )


# ── TC-B-21 to B-22: SKIP (API-only) ─────────────────────────────────────────

@pytest.mark.skip(
    reason="TC-B-21: API-only — extreme qty (INT_MAX) via dead /api/cart endpoint. "
           "Test via: POST /api/cart {quantity: 2147483647}."
)
@pytest.mark.cart_domain
def test_TC_B_21_api_cart_extreme_qty(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-22: API-only — XSS in shipping_address via POST /api/checkout. "
           "Test via: POST /api/checkout {shipping_address: '<script>alert(1)</script>'}."
)
@pytest.mark.cart_domain
def test_TC_B_22_api_checkout_xss_shipping(driver):
    pass


# ══════════════════════════════════════════════════════════════════════════════
# TC-B-23 to TC-B-29: UI-reachable tests added during critical review
# ══════════════════════════════════════════════════════════════════════════════

# ── TC-B-23: Price manipulation via editable checkout total (CRITICAL) ────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-02 (Critical): Checkout.jsx renders total as <input type='number'> "
           "that users can freely edit. Server accepts any total_amount without "
           "verifying against cart contents. CORRECT expectation: server should reject "
           "or recalculate. This test will PASS (i.e. become XPASS) once fixed."
)
@pytest.mark.cart_domain
def test_TC_B_23_price_manipulation_editable_total(logged_in_driver):
    """TC-B-23 — Add high-value product, edit checkout total to 1, confirm.
    CORRECT assertion: server REJECTS the manipulated total. Currently XFAIL (BUG-B-02)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)  # iPhone 15 Pro Max: 30,000,000
    home.click_cart_nav()
    CartPage(logged_in_driver).wait_for_load().click_checkout()

    checkout = CheckoutPage(logged_in_driver).wait_for_load()
    original_total = checkout.get_total_value()
    assert int(original_total) > 1, f"Original total must be >1 to test manipulation (got {original_total})"

    checkout.set_total(1).confirm_order()
    # CORRECT: manipulated total should be rejected
    assert not checkout.is_success(), (
        f"BUG-B-02: Checkout accepted total=1 instead of {original_total}. "
        "Server never verifies total_amount against cart contents."
    )


# ── TC-B-24: Every UI order has NULL shipping_address (BUG-B-06) ──────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-06: UI checkout body never includes shipping_address → stored as NULL. "
           "Every UI order is undeliverable. CORRECT: checkout should require an address."
)
@pytest.mark.cart_domain
def test_TC_B_24_ui_order_has_null_shipping_address(logged_in_driver):
    """TC-B-24 — Complete a normal checkout and verify shipping_address in DB.
    CORRECT assertion: shipping_address is not NULL. Currently XFAIL (BUG-B-06)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.add_product_to_cart(0)
    home.click_cart_nav()
    CartPage(logged_in_driver).wait_for_load().click_checkout()

    checkout = CheckoutPage(logged_in_driver).wait_for_load()
    checkout.confirm_order()
    assert checkout.is_success(), "Checkout should succeed as a prerequisite for this test"

    order = db_get_last_order()
    assert order is not None, "Expected an order to be saved in DB"
    assert order["shipping_address"] is not None, (
        f"BUG-B-06: shipping_address is NULL for every UI order. "
        "Web checkout body: {{items, total_amount, coupon_id}} — no address field. "
        "Server reads req.body.shipping_address → undefined → NULL."
    )


# ── TC-B-25: Web quantity = NaN / empty (no guard) — BUG-B-07 ────────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-07: ProductDetail.jsx uses parseInt(quantity) with NO NaN/≤0 guard. "
           "Empty quantity field → parseInt('') = NaN → quantity=NaN stored in cart. "
           "CORRECT: coerce to ≥1 or show error. Mobile has normalizeQuantity; web does not."
)
@pytest.mark.cart_domain
def test_TC_B_25_web_nan_quantity_rejected(logged_in_driver):
    """TC-B-25 — Navigate to product detail, clear qty field, add to cart.
    CORRECT: should coerce to 1 or reject. Currently XFAIL: NaN stored in cart (BUG-B-07)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.click_first_product_detail()  # React Router nav

    detail = ProductDetailPage(logged_in_driver)
    WebDriverWait(logged_in_driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'bg-green-600')]"))
    )
    detail.clear_quantity()
    detail.add_to_cart()
    detail.click_cart_nav()

    cart = CartPage(logged_in_driver).wait_for_load()
    qty_text = cart.get_item_quantity_text(0)
    # CORRECT: qty should be ≥1 (not NaN / empty). XFAIL until fixed.
    assert qty_text not in ("", "NaN"), (
        f"BUG-B-07: Empty qty field → parseInt('')=NaN stored in cart. "
        f"Actual qty in cart: '{qty_text}'. Web has no normalizeQuantity guard."
    )


# ── TC-B-26: Web zero / negative quantity (no guard) — BUG-B-07 ──────────────

@pytest.mark.xfail(
    strict=False,
    reason="BUG-B-07: Web ProductDetail has no quantity guard. qty=0 → total=0. "
           "CORRECT: coerce to ≥1 or reject."
)
@pytest.mark.cart_domain
def test_TC_B_26_web_zero_quantity_rejected(logged_in_driver):
    """TC-B-26 — Set qty=0 in product detail, add to cart.
    CORRECT: should coerce to 1 or reject. Currently XFAIL: qty=0 stored (BUG-B-07)."""
    home = HomePage(logged_in_driver).wait_for_products()
    home.click_first_product_detail()

    detail = ProductDetailPage(logged_in_driver)
    WebDriverWait(logged_in_driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'bg-green-600')]"))
    )
    detail.set_quantity(0)
    detail.add_to_cart()
    detail.click_cart_nav()

    cart = CartPage(logged_in_driver).wait_for_load()
    qty_text = cart.get_item_quantity_text(0)
    # CORRECT: qty ≥ 1
    assert qty_text not in ("0", ""), (
        f"BUG-B-07: qty=0 stored in web cart without normalization. "
        f"Actual qty: '{qty_text}'."
    )


# ── TC-B-27: SKIP (mobile off-by-one inline editor) ──────────────────────────

@pytest.mark.skip(
    reason="TC-B-27: Mobile-only — BUG-B-08: inline cart qty editor in App.js:617-619 "
           "computes `parsed + 1` instead of `parsed`. Typing 5 stores 6. Requires Appium."
)
@pytest.mark.cart_domain
def test_TC_B_27_mobile_inline_qty_offbyone(driver):
    pass


# ── TC-B-28: Cart cleared on page refresh ─────────────────────────────────────

@pytest.mark.cart_domain
def test_TC_B_28_cart_cleared_on_refresh(driver):
    """TC-B-28 — Add product, refresh page, verify cart is empty.
    Expected: cart clears (React useState, no localStorage persistence) — BUG-B-03."""
    home = HomePage(driver).open()
    home.add_product_to_cart(0)
    home.click_cart_nav()

    cart_before = CartPage(driver).wait_for_load()
    assert not cart_before.is_empty(), "Item should be in cart before refresh"

    # Full page refresh — React state reinitialises to []
    driver.refresh()
    WebDriverWait(driver, 6).until(
        lambda d: "đang trống" in d.page_source or "/cart" in d.current_url
    )
    cart_after = CartPage(driver).wait_for_load()
    assert cart_after.is_empty(), (
        "BUG-B-03: Cart (React useState) is not persisted to localStorage or backend. "
        "All items are lost on page refresh."
    )


# ── TC-B-29: SKIP (mobile drops last item in checkout body) ──────────────────

@pytest.mark.skip(
    reason="TC-B-29: Mobile-only — App.js checkout body uses cart.slice(0,-1) when "
           "cart.length>1, silently dropping the last item. Latent (server ignores items). "
           "Requires Appium."
)
@pytest.mark.cart_domain
def test_TC_B_29_mobile_checkout_drops_last_item(driver):
    pass


# ══════════════════════════════════════════════════════════════════════════════
# OWASP Constraint Test Cases (TC-B-C-01 to TC-B-C-04): SKIP (API-only)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skip(
    reason="TC-B-C-01: API security test — price manipulation via crafted POST /api/cart "
           "(dead endpoint). Test via curl: POST /api/cart {price:1} then POST /api/checkout "
           "{total_amount:1}. BUG-B-05."
)
@pytest.mark.cart_domain
def test_TC_B_C_01_owasp_price_manipulation_api(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-C-02: API security test — total_amount bypass at checkout. "
           "The UI equivalent is TC-B-23 (editable input). API test: POST /api/checkout "
           "{total_amount:1} while cart has items worth 500,000."
)
@pytest.mark.cart_domain
def test_TC_B_C_02_owasp_total_bypass_api(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-C-03: API access control — GET /api/cart without token. "
           "Test via curl. Expected: 401. Note: the endpoint is dead (no UI caller)."
)
@pytest.mark.cart_domain
def test_TC_B_C_03_owasp_cart_auth_api(driver):
    pass


@pytest.mark.skip(
    reason="TC-B-C-04: API injection — XSS payload in product name stored via dead "
           "/api/cart endpoint. Test via curl: POST /api/cart {name: '<img onerror=alert(1)>'}."
)
@pytest.mark.cart_domain
def test_TC_B_C_04_owasp_xss_cart_name_api(driver):
    pass
