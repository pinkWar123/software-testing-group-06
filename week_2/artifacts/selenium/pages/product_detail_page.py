"""
pages/product_detail_page.py — Page Object for EShop product detail page.

URL: http://localhost:5173/product/{id}

KEY BUG — double-click required (BUG-B-09, not yet in report):
  handleAddToCart() in ProductDetail.jsx:
    Click 1 → clickCount 0→1 (silent no-op)
    Click 2 → clickCount 1→0, item added, button text → 'Đã thêm' for 2 s

  add_to_cart() accounts for this by clicking twice.

Quantity handling:
  onChange: setQuantity(e.target.value)   [stored as string]
  onClick:  addToCart(product, parseInt(quantity))
  - Empty field:  parseInt('') = NaN → quantity=NaN in cart  (BUG-B-07)
  - '0':          parseInt('0') = 0  → quantity=0            (BUG-B-07)
  - '-3':         parseInt('-3') = -3 → quantity=-3          (BUG-B-07)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://localhost:5173"


class ProductDetailPage:
    _TITLE      = (By.TAG_NAME, "h1")
    _PRICE      = (By.XPATH, "//p[contains(@class,'text-2xl') and contains(@class,'text-red-600')]")
    _QTY_INPUT  = (By.XPATH, "//label[text()='Số lượng:']/following-sibling::input[@type='number']")
    _ADD_BTN    = (By.XPATH, "//button[contains(@class,'bg-green-600')]")
    _ADDED_BTN  = (By.XPATH, "//button[text()='Đã thêm']")
    _CART_NAV   = (By.XPATH, "//a[text()='Giỏ hàng']")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver  = driver
        self.wait    = WebDriverWait(driver, timeout)

    def open(self, product_id: int) -> "ProductDetailPage":
        self.driver.get(f"{BASE_URL}/product/{product_id}")
        self.wait.until(EC.presence_of_element_located(self._ADD_BTN))
        return self

    def set_quantity(self, value) -> "ProductDetailPage":
        """Set the quantity input to `value` (int, float, or str)."""
        field = self.wait.until(EC.element_to_be_clickable(self._QTY_INPUT))
        field.clear()
        field.send_keys(str(value))
        return self

    def clear_quantity(self) -> "ProductDetailPage":
        """Clear the quantity field entirely (results in NaN when added)."""
        field = self.wait.until(EC.element_to_be_clickable(self._QTY_INPUT))
        field.clear()
        return self

    def add_to_cart(self) -> "ProductDetailPage":
        """Add item to cart — requires TWO clicks due to ProductDetail.jsx bug.

        Click 1: clickCount 0→1 (no-op — button does not react visibly)
        Click 2: item added, button text changes to 'Đã thêm'
        """
        btn = self.wait.until(EC.element_to_be_clickable(self._ADD_BTN))
        btn.click()
        # Re-find after React re-render (clickCount state change)
        btn = self.wait.until(EC.element_to_be_clickable(self._ADD_BTN))
        btn.click()
        return self

    def is_added(self) -> bool:
        """True if button text is 'Đã thêm' — confirms item was added on 2nd click."""
        try:
            WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located(self._ADDED_BTN)
            )
            return True
        except TimeoutException:
            return False

    def click_cart_nav(self) -> None:
        """Click 'Giỏ hàng' in the header (React Router, preserves cart state)."""
        self.wait.until(EC.element_to_be_clickable(self._CART_NAV)).click()

    def get_product_title(self) -> str:
        return self.driver.find_element(*self._TITLE).text.strip()
