from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object representing the application's login page."""

    def __init__(self, page: Page) -> None:
        # Initialize reusable browser methods from BasePage.
        super().__init__(page)

        # Define locators for elements on the login page.
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_test_id("login-error")

    def open(self, base_url: str) -> None:
        """Open the login page."""
        self.navigate(f"{base_url}/login")

    def login(self, username: str, password: str) -> None:
        """Submit the supplied credentials."""
        # Enter the username into the username field.
        self.username_input.fill(username)

        # Enter the password into the password field.
        self.password_input.fill(password)

        # Submit the login form.
        self.login_button.click()

    def assert_login_error(self, message: str) -> None:
        """Verify that the expected login error is displayed."""
        # Check that the error message is visible and contains
        # the expected text.
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(message)
