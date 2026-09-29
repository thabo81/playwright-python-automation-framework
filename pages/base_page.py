from playwright.sync_api import Page


class BasePage:
    """Base Page Object containing reusable browser actions."""

    def __init__(self, page: Page) -> None:
        # Store the Playwright Page object so all child Page Objects
        # can interact with the browser through self.page.
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate the browser to the specified URL."""
        self.page.goto(url)

    def refresh(self) -> None:
        """Refresh the current browser page."""
        self.page.reload()

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()