import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
def test_home_page_displays_user(
    home_page: HomePage,
    test_app_url: str,
) -> None:
    """Verify that the home page displays the expected user."""

    # Navigate to the application under test.
    home_page.navigate(test_app_url)

    # Verify that the home page loaded correctly.
    home_page.assert_loaded()

    # Verify that the expected user information is displayed.
    home_page.assert_user("Demo User", "SDET")
