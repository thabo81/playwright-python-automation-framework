from playwright.sync_api import Page, expect


class HomePage:
    """Page Object for the local automation demo page."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.get_by_test_id("page-title")
        self.user_name = page.get_by_test_id("user-name")
        self.user_role = page.get_by_test_id("user-role")

    def open(self, base_url: str) -> None:
        self.page.goto(base_url)

    def assert_loaded(self) -> None:
        expect(self.title).to_have_text("Playwright Automation Demo")

    def assert_user(self, name: str, role: str) -> None:
        expect(self.user_name).to_have_text(name)
        expect(self.user_role).to_have_text(role)
