from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page Object representing the authenticated dashboard."""

    def __init__(self, page: Page) -> None:
        # Initialize shared browser actions from BasePage.
        super().__init__(page)

        # Define locators used only by the dashboard.
        self.dashboard_title = page.get_by_test_id("dashboard-title")
        self.welcome_message = page.get_by_test_id("welcome-message")
        self.logout_button = page.get_by_test_id("logout-button")

    def assert_loaded(self) -> None:
        """Verify that the authenticated dashboard is displayed."""
        # Confirm that the dashboard heading is visible and correct.
        expect(self.dashboard_title).to_have_text("Dashboard")

    def assert_welcome_message(self, username: str) -> None:
        """Verify that the expected user is welcomed."""
        # Validate the text shown to the authenticated user.
        expect(self.welcome_message).to_have_text(
            f"Welcome, {username}"
        )
