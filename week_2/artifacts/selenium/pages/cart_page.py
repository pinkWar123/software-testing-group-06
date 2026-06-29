"""
pages/cart_page.py — Page Object for the EShop cart page.

URL: http://localhost:5173/cart

Key observations from Cart.jsx:
  - Empty cart: renders h2 containing 'đang trống', no checkout button
  - Non-empty: renders a <table> with one <tr> per cart item
    Columns: name | price | quantity | subtotal | remove
  - Cart total: <span class="text-red-600"> inside the flex footer
  - 'Tiến hành thanh toán' button triggers an alert + redirect to /login
    if user is not authenticated, otherwise React-Routers to /checkout.
  - Cart state is ONLY in React memory — navigating away (driver.get) clears it.
    Always use click_cart_nav() (header link) to preserve state.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://localhost:5173"


class CartPage:
    _EMPTY_MSG      = (By.XPATH, "//h2[contains(text(),'đang trống')]")
    _TABLE_ROWS     = (By.XPATH, "//tbody/tr")
    _CART_TOTAL_EL  = (By.XPATH, "//div[contains(@class,'text-xl')]//span[contains(@class,'text-red-600')]")
    _CHECKOUT_BTN   = (By.XPATH, "//button[contains(text(),'Tiến hành thanh toán')]")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver  = driver
        self.wait    = WebDriverWait(driver, timeout)

    def open(self) -> "CartPage":
        """Full-page navigate — CLEARS React cart state. Use only for empty-cart tests."""
        self.driver.get(f"{BASE_URL}/cart")
        return self

    def wait_for_load(self) -> "CartPage":
        """Wait for the cart page to render after client-side navigation."""
        try:
            self.wait.until(
                lambda d: d.current_url.endswith("/cart")
                or "đang trống" in d.page_source
                or d.find_elements(By.XPATH, "//tbody/tr")
            )
        except TimeoutException:
            pass
        return self

    def is_empty(self) -> bool:
        try:
            self.driver.find_element(*self._EMPTY_MSG)
            return True
        except Exception:
            return False

    def get_row_count(self) -> int:
        return len(self.driver.find_elements(*self._TABLE_ROWS))

    def _get_row_cells(self, row: int):
        rows = self.driver.find_elements(*self._TABLE_ROWS)
        if row >= len(rows):
            return []
        return rows[row].find_elements(By.TAG_NAME, "td")

    def get_item_name(self, row: int = 0) -> str:
        cells = self._get_row_cells(row)
        return cells[0].text.strip() if cells else ""

    def get_item_price_text(self, row: int = 0) -> str:
        cells = self._get_row_cells(row)
        return cells[1].text.strip() if len(cells) > 1 else ""

    def get_item_quantity_text(self, row: int = 0) -> str:
        cells = self._get_row_cells(row)
        return cells[2].text.strip() if len(cells) > 2 else ""

    def get_item_subtotal_text(self, row: int = 0) -> str:
        cells = self._get_row_cells(row)
        return cells[3].text.strip() if len(cells) > 3 else ""

    def get_cart_total_text(self) -> str:
        try:
            el = self.wait.until(EC.visibility_of_element_located(self._CART_TOTAL_EL))
            return el.text.strip()
        except TimeoutException:
            return ""

    @staticmethod
    def parse_vnd(text: str) -> float:
        """Parse '30,000,000 ₫' → 30000000.0; returns float('nan') on failure."""
        import math
        cleaned = text.replace("₫", "").replace(",", "").replace(".", "").replace(" ", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return float("nan")

    def click_checkout(self) -> None:
        """Click checkout; accept the alert if user is not logged in."""
        self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BTN)).click()
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
        except Exception:
            pass

    def is_on_cart_page(self) -> bool:
        return "/cart" in self.driver.current_url

    def is_on_login_page(self) -> bool:
        return "/login" in self.driver.current_url
