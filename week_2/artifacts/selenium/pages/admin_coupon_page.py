"""
pages/admin_coupon_page.py — Page Object for Admin Coupon Management (FR-17).

URL: http://localhost:5174  (admin frontend; click "Mã Giảm Giá" tab after login)

Key UI elements observed from App.jsx:
  Sidebar nav item: <li onClick={() => setActiveTab("coupons")}>Mã Giảm Giá</li>

  Create form (all inside the coupons tab):
    code input      : placeholder "Mã coupon (VD: SAVE10)"  — required; uppercases on change
    type select     : <select> with options percent (Phần trăm) / fixed (Số tiền cố định)
    discount_value  : type="number", required; placeholder changes with type
    min_order_amount: type="number", placeholder "Đơn tối thiểu (₫)"
    expired_at      : type="date", required
    max_uses_per_user: type="number", min="1"
    submit button   : class bg-orange-500, text "Tạo mã"

  Error feedback  : browser alert() dialog (e.g. on duplicate code → 500 from backend)

  Coupon table columns: Mã | Loại | Giá trị | Đơn tối thiểu | Hết hạn | Giới hạn/người | Hành động
    Expired indicator : <span class="text-red-500">Hết hạn</span>
    Delete button     : class bg-red-500, text "Xóa" (one per row)
"""
from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ADMIN_URL = "http://localhost:5174"


class AdminCouponPage:
    # ── Sidebar ────────────────────────────────────────────────────────────────
    _COUPON_NAV  = (By.XPATH, "//li[contains(text(),'Mã Giảm Giá')]")

    # ── Create form ────────────────────────────────────────────────────────────
    _CODE_INPUT  = (By.CSS_SELECTOR, "input[placeholder='Mã coupon (VD: SAVE10)']")
    _TYPE_SELECT = (By.CSS_SELECTOR, "select")
    _VALUE_INPUT = (By.XPATH, "//input[@type='number' and (@placeholder='Giá trị % (VD: 10)' or @placeholder='Số tiền (VD: 50000)')]")
    _MIN_INPUT   = (By.CSS_SELECTOR, "input[placeholder='Đơn tối thiểu (₫)']")
    _DATE_INPUT  = (By.CSS_SELECTOR, "input[type='date']")
    _MAX_INPUT   = (By.CSS_SELECTOR, "input[placeholder='Số lần dùng tối đa/người']")
    _SUBMIT_BTN  = (By.XPATH, "//button[text()='Tạo mã']")

    # ── Table ──────────────────────────────────────────────────────────────────
    _TABLE_ROWS     = (By.CSS_SELECTOR, "table tbody tr")
    _EXPIRED_BADGES = (By.CSS_SELECTOR, "span.text-red-500")
    _DELETE_BTNS    = (By.XPATH, "//button[text()='Xóa']")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def navigate_to_coupons_tab(self) -> "AdminCouponPage":
        """Click the 'Mã Giảm Giá' sidebar item and wait for the form to appear."""
        self.wait.until(EC.element_to_be_clickable(self._COUPON_NAV)).click()
        self.wait.until(EC.presence_of_element_located(self._CODE_INPUT))
        return self

    # ── Form helpers ───────────────────────────────────────────────────────────

    def set_code(self, value: str) -> "AdminCouponPage":
        field = self.wait.until(EC.element_to_be_clickable(self._CODE_INPUT))
        field.clear()
        field.send_keys(value)
        return self

    def set_type(self, value: str) -> "AdminCouponPage":
        """value: 'percent' or 'fixed'."""
        sel = Select(self.wait.until(EC.element_to_be_clickable(self._TYPE_SELECT)))
        sel.select_by_value(value)
        return self

    def get_type_options(self) -> list[str]:
        """Return all option values from the type dropdown."""
        sel = Select(self.wait.until(EC.presence_of_element_located(self._TYPE_SELECT)))
        return [o.get_attribute("value") for o in sel.options]

    def get_discount_value_placeholder(self) -> str:
        field = self.wait.until(EC.presence_of_element_located(self._VALUE_INPUT))
        return field.get_attribute("placeholder") or ""

    def set_discount_value(self, value: str | int) -> "AdminCouponPage":
        field = self.wait.until(EC.element_to_be_clickable(self._VALUE_INPUT))
        field.clear()
        field.send_keys(str(value))
        return self

    def set_min_order(self, value: str | int) -> "AdminCouponPage":
        field = self.wait.until(EC.element_to_be_clickable(self._MIN_INPUT))
        field.clear()
        field.send_keys(str(value))
        return self

    def set_expired_at(self, date_iso: str) -> "AdminCouponPage":
        """Set the date input; date_iso in 'YYYY-MM-DD' format.

        Uses the native HTMLInputElement.prototype.value setter then dispatches
        bubbling input + change events — this is required to trigger React's
        synthetic event handler (direct .value assignment is ignored by React).
        """
        field = self.wait.until(EC.element_to_be_clickable(self._DATE_INPUT))
        self.driver.execute_script(
            """
            var el = arguments[0];
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input',  { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            field, date_iso,
        )
        return self

    def set_max_uses(self, value: str | int) -> "AdminCouponPage":
        field = self.wait.until(EC.element_to_be_clickable(self._MAX_INPUT))
        self.driver.execute_script("arguments[0].value = ''", field)
        field.send_keys(str(value))
        return self

    def click_submit(self) -> "AdminCouponPage":
        self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()
        return self

    def submit_form(
        self,
        code: str,
        type_: str = "percent",
        discount_value: str | int = 10,
        min_order: str | int = 0,
        expired_at: str = "2099-12-31",
        max_uses: str | int = 1,
    ) -> "AdminCouponPage":
        """Fill all fields and click 'Tạo mã'."""
        self.set_code(code)
        self.set_type(type_)
        self.set_discount_value(discount_value)
        self.set_min_order(min_order)
        self.set_expired_at(expired_at)
        self.set_max_uses(max_uses)
        self.click_submit()
        return self

    # ── Alert handling ─────────────────────────────────────────────────────────

    def dismiss_alert(self, timeout: float = 3.0) -> str | None:
        """Accept any pending browser alert and return its text; None if no alert."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text  = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None

    # ── Table read helpers ─────────────────────────────────────────────────────

    def get_coupon_codes_in_table(self) -> list[str]:
        """Return all coupon codes currently rendered in the table."""
        rows = self.driver.find_elements(*self._TABLE_ROWS)
        codes = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                codes.append(cells[0].text.strip())
        return codes

    def get_row_for_code(self, code: str):
        """Return the <tr> element whose first cell matches `code`, or None."""
        rows = self.driver.find_elements(*self._TABLE_ROWS)
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == code:
                return row
        return None

    def get_expiry_cell_text(self, code: str) -> str:
        """Return the text of the Hết hạn column for a coupon by code."""
        row = self.get_row_for_code(code)
        if row is None:
            return ""
        cells = row.find_elements(By.TAG_NAME, "td")
        return cells[4].text.strip() if len(cells) > 4 else ""

    def is_code_in_table(self, code: str) -> bool:
        return self.get_row_for_code(code) is not None

    def count_expired_badges(self) -> int:
        return len(self.driver.find_elements(*self._EXPIRED_BADGES))

    def delete_coupon_by_code(self, code: str) -> bool:
        """Click the Xóa button for the row matching `code`. Returns True if clicked."""
        row = self.get_row_for_code(code)
        if row is None:
            return False
        row.find_element(By.XPATH, ".//button[text()='Xóa']").click()
        return True

    def wait_for_row_gone(self, code: str, timeout: int = 5) -> bool:
        """Wait until the coupon code is no longer in the table.

        Catches StaleElementReferenceException — React re-renders the table after
        deletion, invalidating previously cached element references.
        """
        from selenium.common.exceptions import StaleElementReferenceException

        def _gone(driver):
            try:
                return not self.is_code_in_table(code)
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, timeout).until(_gone)
            return True
        except TimeoutException:
            return False

    def wait_for_row_present(self, code: str, timeout: int = 5) -> bool:
        """Wait until the coupon code appears in the table."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.is_code_in_table(code)
            )
            return True
        except TimeoutException:
            return False

    def is_form_valid(self) -> bool:
        """Check HTML5 validity of the create form (returns True if no constraint errors)."""
        return self.driver.execute_script(
            "return document.querySelector('form').checkValidity()"
        )

    def get_field_validation_message(self, selector: str) -> str:
        return self.driver.execute_script(
            "return document.querySelector(arguments[0]).validationMessage",
            selector,
        ) or ""
