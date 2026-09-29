from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object representing the application's home page."""

    def __init__(self, page: Page) -> None:
        # Call BasePage so we inherit common browser actions.
        super().__init__(page)

        # Define locators specific to the Home Page.
        self.page_title = page.get_by_test_id("page-title")
        self.user_name = page.get_by_test_id("user-name")
        self.user_role = page.get_by_test_id("user-role")

    def assert_loaded(self) -> None:
        """Verify that the home page loaded successfully."""
        expect(self.page_title).to_have_text(
            "Playwright Automation Demo"
        )

    def assert_user(self, name: str, role: str) -> None:
        """Verify the user information displayed on the page."""
        expect(self.user_name).to_have_text(name)
        expect(self.user_role).to_have_text(role)
