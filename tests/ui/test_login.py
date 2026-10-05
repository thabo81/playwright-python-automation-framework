import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(
    page: Page,
    test_app_url: str,
) -> None:
    """Verify that valid credentials redirect the user to the dashboard."""
    login_page = LoginPage(page)

    # Open the login page.
    login_page.open(test_app_url)

    # Submit the known valid test credentials.
    login_page.login("testuser", "Password123")

    # Verify that a successful login redirects to the dashboard.
    page.wait_for_url("**/dashboard")
    assert page.url.endswith("/dashboard")


@pytest.mark.ui
def test_invalid_password_displays_error(
    page: Page,
    test_app_url: str,
) -> None:
    """Verify that an invalid password is rejected."""
    login_page = LoginPage(page)

    # Open the login page.
    login_page.open(test_app_url)

    # Submit a valid username with an invalid password.
    login_page.login("testuser", "WrongPassword")

    # Verify that the expected authentication error is shown.
    login_page.assert_login_error("Invalid username or password")


@pytest.mark.ui
def test_empty_credentials_displays_validation_error(
    page: Page,
    test_app_url: str,
) -> None:
    """Verify that empty credentials are rejected."""
    login_page = LoginPage(page)

    # Open the login page.
    login_page.open(test_app_url)

    # Submit blank credentials.
    login_page.login("", "")

    # Verify that the expected validation error is shown.
    login_page.assert_login_error("Username and password are required")
