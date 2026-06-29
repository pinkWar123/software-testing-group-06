"""
pages/home_page.py — Page Object for the EShop home / product-listing page.

URL: http://localhost:5173/

Key observations from Home.jsx:
  - Products rendered in a 3-column grid; each card has:
      "Xem chi tiết" link  → /product/{id}  (React Router)
      "Thêm vào giỏ" btn   → addToCart({ ...p, quantity: 1 }, 1)  (one click, no double-click)
  - The home-page add-to-cart does NOT require a double click (unlike ProductDetail).
  - Items are added to the CartContext React state (client-side) — NOT to /api/cart.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5173"


class HomePage:
    _ADD_BTN     = (By.XPATH, "//button[text()='Thêm vào giỏ']")
    _DETAIL_LINK = (By.XPATH, "//a[text()='Xem chi tiết']")
    _PRICE_TEXTS = (By.XPATH, "//p[contains(@class,'text-red-500')]")
    _CART_NAV    = (By.XPATH, "//a[text()='Giỏ hàng']")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver  = driver
        self.wait    = WebDriverWait(driver, timeout)

    def open(self) -> "HomePage":
        self.driver.get(BASE_URL)
        self.wait.until(EC.presence_of_all_elements_located(self._ADD_BTN))
        return self

    def wait_for_products(self) -> "HomePage":
        """Wait for products grid without triggering a page navigation."""
        self.wait.until(EC.presence_of_all_elements_located(self._ADD_BTN))
        return self

    def product_count(self) -> int:
        return len(self.driver.find_elements(*self._ADD_BTN))

    def add_product_to_cart(self, index: int = 0) -> "HomePage":
        """Click 'Thêm vào giỏ' for the nth product (0-indexed, single click)."""
        btns = self.wait.until(EC.presence_of_all_elements_located(self._ADD_BTN))
        btns[index].click()
        return self

    def click_first_product_detail(self) -> None:
        """Navigate to the first product's detail page via React Router."""
        links = self.wait.until(EC.presence_of_all_elements_located(self._DETAIL_LINK))
        links[0].click()

    def get_first_product_price_text(self) -> str:
        """Return raw price string for first product, e.g. '30,000,000 VND'."""
        els = self.wait.until(EC.presence_of_all_elements_located(self._PRICE_TEXTS))
        return els[0].text.strip() if els else ""

    def click_cart_nav(self) -> None:
        """Click 'Giỏ hàng' in the header (React Router, preserves cart state)."""
        self.wait.until(EC.element_to_be_clickable(self._CART_NAV)).click()
