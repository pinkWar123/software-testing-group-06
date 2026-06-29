"""
pages/checkout_page.py — Page Object for the EShop checkout page.

URL: http://localhost:5173/checkout

Key observations from Checkout.jsx:
  - editableTotal is initialised from cartTotal and rendered as <input type='number'>
    at line 93-102: the user CAN edit this field. (→ BUG-B-02)
  - The checkout body is: { items: cart, total_amount: finalAmount, coupon_id: ... }
    — NO shipping_address field. (→ BUG-B-06)
  - On success, setSuccess(true) shows success screen (URL stays /checkout).
  - Coupon section not tested here.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

BASE_URL = "http://localhost:5173"


class CheckoutPage:
    _TOTAL_INPUT    = (By.XPATH, "//label[contains(text(),'Tổng tiền')]/following-sibling::input[@type='number']")
    _CONFIRM_BTN    = (By.XPATH, "//button[contains(text(),'Xác Nhận Thanh Toán')]")
    _SUCCESS_H2     = (By.XPATH, "//h2[contains(text(),'Thanh toán thành công')]")
    _ITEM_LIST      = (By.XPATH, "//ul/li")
    # Shipping address input — expected to NOT exist (BUG-B-06)
    _SHIPPING_INPUT = (By.XPATH,
        "//input[@type='text' and (preceding::label[contains(text(),'địa chỉ')]"
        " or preceding::label[contains(text(),'giao hàng')])]"
    )

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver  = driver
        self.wait    = WebDriverWait(driver, timeout)

    def open(self) -> "CheckoutPage":
        """Full-page navigate — ONLY use for empty-cart scenario (TC-B-16)."""
        self.driver.get(f"{BASE_URL}/checkout")
        self.wait.until(EC.presence_of_element_located(self._CONFIRM_BTN))
        return self

    def wait_for_load(self) -> "CheckoutPage":
        """Wait after React Router navigation from cart."""
        self.wait.until(EC.presence_of_element_located(self._CONFIRM_BTN))
        return self

    def get_total_value(self) -> str:
        """Return the current value of the editable total input."""
        el = self.wait.until(EC.presence_of_element_located(self._TOTAL_INPUT))
        return el.get_attribute("value")

    def set_total(self, value) -> "CheckoutPage":
        """Overwrite the editable total input with an arbitrary value (BUG-B-02 exploit)."""
        el = self.wait.until(EC.element_to_be_clickable(self._TOTAL_INPUT))
        el.clear()
        el.send_keys(str(value))
        return self

    def confirm_order(self) -> "CheckoutPage":
        self.wait.until(EC.element_to_be_clickable(self._CONFIRM_BTN)).click()
        return self

    def is_success(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self._SUCCESS_H2))
            return True
        except TimeoutException:
            return False

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self._ITEM_LIST))

    def has_shipping_address_field(self) -> bool:
        """Should return False — verifies BUG-B-06 (UI never asks for address)."""
        return len(self.driver.find_elements(*self._SHIPPING_INPUT)) > 0

    def is_on_checkout_page(self) -> bool:
        return "/checkout" in self.driver.current_url
