import pytest
from pages.login_page import LoginPage
from utils.data_reader import read_login_data


class TestLoginDataDriven:
    """
    Data-driven login tests using CSV file.
    One test function runs once per row in login_data.csv.
    Adding new test cases = adding new row in CSV only.
    No code change needed!
    """

    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, expected, test_id",
        read_login_data()
    )
    def test_login_with_csv_data(
            self, driver, username,
            password, expected, test_id):
        """
        Runs once per row in login_data.csv.
        TC01 = valid login
        TC02 = locked user
        TC03 = wrong password
        TC04 = empty username
        TC05 = empty password
        TC06 = problem user
        TC07 = performance glitch user
        """
        page = LoginPage(driver)
        page.login(username, password)

        if expected == "success":
            assert page.is_logged_in(), \
                f"{test_id}: Login should succeed for '{username}'"
        else:
            error = page.get_error_message()
            assert expected.lower() in error.lower(), \
                f"{test_id}: Expected '{expected}' in error, got: '{error}'"