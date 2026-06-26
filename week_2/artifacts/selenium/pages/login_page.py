"""
pages/login_page.py — Page Object Model for the EShop login page.

URL: http://localhost:5173/login

Observed UI elements (from Login.jsx + screenshot):
  - h2 title: "Đăng Ký"  ← known UI bug (should be "Đăng Nhập")
  - Label "Username"    → input type="text"   (internal var: email)
  - Label "Mật khẩu"   → input type="text"   ← known bug (should be type="password")
  - Link  "Quên mật khẩu?"
  - Button "Sign In"   (type="submit")
  - Link  "Đăng ký ngay"
  - Error div (class bg-red-100): "Đăng nhập thất bại. Vui lòng kiểm tra lại."
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5173"


class LoginPage:
    # ── Locators ───────────────────────────────────────────────────────────────
    _USERNAME_INPUT   = (By.XPATH, "//label[text()='Username']/following-sibling::input")
    _PASSWORD_INPUT   = (By.XPATH, "//label[contains(text(),'Mật khẩu')]/following-sibling::input")
    _SIGN_IN_BUTTON   = (By.XPATH, "//button[@type='submit']")
    _ERROR_DIV        = (By.XPATH, "//div[contains(@class,'bg-red-100')]")
    _H2_TITLE         = (By.TAG_NAME, "h2")
    _FORGOT_PW_LINK   = (By.XPATH, "//a[contains(text(),'Quên mật khẩu')]")
    _REGISTER_LINK    = (By.XPATH, "//a[contains(text(),'Đăng ký ngay')]")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ── Navigation ─────────────────────────────────────────────────────────────
    def open(self) -> "LoginPage":
        self.driver.get(f"{BASE_URL}/login")
        self.wait.until(EC.presence_of_element_located(self._SIGN_IN_BUTTON))
        return self

    # ── Actions ────────────────────────────────────────────────────────────────
    def enter_username(self, value: str) -> "LoginPage":
        field = self.wait.until(EC.element_to_be_clickable(self._USERNAME_INPUT))
        field.clear()
        field.send_keys(value)
        return self

    def enter_password(self, value: str) -> "LoginPage":
        field = self.wait.until(EC.element_to_be_clickable(self._PASSWORD_INPUT))
        field.clear()
        field.send_keys(value)
        return self

    def click_sign_in(self) -> "LoginPage":
        self.wait.until(EC.element_to_be_clickable(self._SIGN_IN_BUTTON)).click()
        return self

    def submit(self, username: str, password: str) -> "LoginPage":
        """Enter both fields and click Sign In."""
        return self.enter_username(username).enter_password(password).click_sign_in()

    # ── Assertions helpers ─────────────────────────────────────────────────────
    def get_error_text(self) -> str:
        """Return the visible error message, or '' if none."""
        try:
            el = self.wait.until(EC.visibility_of_element_located(self._ERROR_DIV))
            return el.text.strip()
        except TimeoutException:
            return ""

    def is_error_shown(self) -> bool:
        return bool(self.get_error_text())

    def is_login_successful(self) -> bool:
        """True when the browser navigates away from /login (success redirect)."""
        try:
            WebDriverWait(self.driver, 6).until(
                lambda d: "/login" not in d.current_url
            )
            return True
        except TimeoutException:
            return False

    def is_still_on_login_page(self) -> bool:
        return "/login" in self.driver.current_url

    def get_h2_title(self) -> str:
        return self.driver.find_element(*self._H2_TITLE).text.strip()

    def get_password_field_type(self) -> str:
        """Returns the HTML 'type' attribute of the password input."""
        field = self.driver.find_element(*self._PASSWORD_INPUT)
        return field.get_attribute("type")

    def get_username_maxlength(self):
        """Returns the maxlength attribute value, or None if not set."""
        return self.driver.find_element(*self._USERNAME_INPUT).get_attribute("maxlength")

    def get_password_maxlength(self):
        """Returns the maxlength attribute value, or None if not set."""
        return self.driver.find_element(*self._PASSWORD_INPUT).get_attribute("maxlength")

    def get_forgot_password_link_href(self) -> str:
        el = self.driver.find_element(*self._FORGOT_PW_LINK)
        return el.get_attribute("href")

    def is_forgot_password_link_visible(self) -> bool:
        try:
            return self.driver.find_element(*self._FORGOT_PW_LINK).is_displayed()
        except Exception:
            return False

    # Expected error message from Login.jsx
    EXPECTED_ERROR_MSG = "Đăng nhập thất bại. Vui lòng kiểm tra lại."
    EXPECTED_H2_TITLE  = "Đăng Nhập"  # correct; actual is "Đăng Ký" (bug)
