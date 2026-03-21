from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for SauceDemo login page.
    URL: https://www.saucedemo.com
    Inherits all Selenium methods from BasePage.
    """

    # ── Locators — defined as class constants ────────────
    USERNAME_INPUT  = (By.ID,   "user-name")
    PASSWORD_INPUT  = (By.ID,   "password")
    LOGIN_BUTTON    = (By.ID,   "login-button")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")
    LOGO            = (By.CLASS_NAME,   "login_logo")

    # ── Actions ──────────────────────────────────────────
    def enter_username(self, username):
        self.type_text(*self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.type_text(*self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(*self.LOGIN_BUTTON)

    def login(self, username, password):
        """Full login action — username + password + click"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Returns error text shown on failed login"""
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_page_displayed(self):
        """Returns True if logo is visible — confirms login page loaded"""
        return self.is_visible(*self.LOGO)

    def is_logged_in(self):
        """Returns True if URL changed to /inventory — login success"""
        return "/inventory" in self.get_current_url()