import pytest
from pages.login_page import LoginPage


class TestLogin:
    """
    Test Suite: Login functionality — SauceDemo
    Site: https://www.saucedemo.com
    """

    # ── TC01: Valid login ────────────────────────────────
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_valid_login(self, driver, config):
        page = LoginPage(driver)
        page.login(
            config["USERS"]["standard_user"],
            config["USERS"]["password"]
        )
        assert page.is_logged_in(), \
            "Login failed — /inventory not in URL"

    # ── TC02: Locked user ────────────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_locked_user_login(self, driver, config):
        page = LoginPage(driver)
        page.login(
            config["USERS"]["locked_user"],
            config["USERS"]["password"]
        )
        error = page.get_error_message()
        assert "locked out" in error.lower(), \
            f"Expected locked error, got: {error}"

    # ── TC03: Wrong password ─────────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_wrong_password(self, driver, config):
        page = LoginPage(driver)
        page.login(
            config["USERS"]["standard_user"],
            "wrongpassword123"
        )
        error = page.get_error_message()
        assert "Username and password do not match" \
               in error, \
            f"Expected mismatch error, got: {error}"

    # ── TC04: Empty username ─────────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_empty_username(self, driver, config):
        page = LoginPage(driver)
        page.login("", config["USERS"]["password"])
        error = page.get_error_message()
        assert "Username is required" in error, \
            f"Expected required error, got: {error}"

    # ── TC05: Empty password ─────────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_empty_password(self, driver, config):
        page = LoginPage(driver)
        page.login(
            config["USERS"]["standard_user"], ""
        )
        error = page.get_error_message()
        assert "Password is required" in error, \
            f"Expected required error, got: {error}"

    # ── TC06: Both fields empty ──────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_empty_username_and_password(self, driver, config):
        page = LoginPage(driver)
        page.login("", "")
        error = page.get_error_message()
        assert "Username is required" in error, \
            f"Expected required error, got: {error}"

    # ── TC07: SQL injection attempt ──────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_sql_injection_in_username(self, driver, config):
        page = LoginPage(driver)
        page.login("' OR '1'='1", "anything")
        error = page.get_error_message()
        assert error is not None and len(error) > 0, \
            "Expected error for SQL injection attempt"

    # ── TC08: Whitespace username ────────────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_whitespace_username(self, driver, config):
        page = LoginPage(driver)
        page.login("   ", config["USERS"]["password"])
        error = page.get_error_message()
        assert error is not None and len(error) > 0, \
            "Expected error for whitespace username"

    # ── TC09: Login then logout ──────────────────────────
    def test_logout_after_login(self, driver, config):
        page = LoginPage(driver)
        page.login(
            config["USERS"]["standard_user"],
            config["USERS"]["password"]
        )
        assert page.is_logged_in(), "Login failed"
        page.logout()
        # Check we are NOT on inventory page anymore
        assert "/inventory" not in driver.current_url, \
            "Expected to leave inventory page after logout"

    # ── TC10: Login page title check ─────────────────────
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_page_title(self, driver, config):
        assert "Swag Labs" in driver.title, \
            f"Expected 'Swag Labs' in title, got: {driver.title}"