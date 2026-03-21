import pytest
from pages.login_page import LoginPage


class TestLogin:
    """
    Test Suite: Login functionality — SauceDemo
    Site: https://www.saucedemo.com
    """

    # ── TC01: Valid login — happy path ───────────────────
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

    # ── TC02: Locked user — negative test ───────────────
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

    # ── TC03: Wrong password — negative test ────────────
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

    # ── TC04: Empty username — edge case ────────────────
    @pytest.mark.ui
    @pytest.mark.regression
    def test_empty_username(self, driver, config):
        page = LoginPage(driver)
        page.login("", config["USERS"]["password"])
        error = page.get_error_message()
        assert "Username is required" in error, \
            f"Expected required error, got: {error}"

    # ── TC05: Empty password — edge case ────────────────
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