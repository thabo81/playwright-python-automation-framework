import pytest

from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(
    login_page: LoginPage,
    test_app_url: str,
) -> None:
    """Verify that valid credentials redirect the user to the dashboard."""

    # Open the login page using the reusable LoginPage fixture.
    login_page.open(test_app_url)

    # Submit the known valid test credentials.
    login_page.login("testuser", "Password123")

    # Wait for the application to navigate after a successful login.
    login_page.page.wait_for_url("**/dashboard")

    # Verify that the final URL is the expected dashboard URL.
    assert login_page.page.url.endswith("/dashboard")


@pytest.mark.ui
def test_invalid_password_displays_error(
    login_page: LoginPage,
    test_app_url: str,
) -> None:
    """Verify that an invalid password is rejected."""

    # Open the login page.
    login_page.open(test_app_url)

    # Submit a valid username with an invalid password.
    login_page.login("testuser", "WrongPassword")

    # Verify that the expected authentication error is displayed.
    login_page.assert_login_error("Invalid username or password")


@pytest.mark.ui
def test_empty_credentials_displays_validation_error(
    login_page: LoginPage,
    test_app_url: str,
) -> None:
    """Verify that empty credentials are rejected."""

    # Open the login page.
    login_page.open(test_app_url)

    # Submit blank credentials.
    login_page.login("", "")

    # Verify that the expected validation error is displayed.
    login_page.assert_login_error("Username and password are required")
