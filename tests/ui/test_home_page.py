import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_displays_user(page: Page, test_app_url: str) -> None:
    home_page = HomePage(page)

    home_page.open(test_app_url)
    home_page.assert_loaded()
    home_page.assert_user("Demo User", "SDET")
