import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.ui
@pytest.mark.smoke
def test_authenticated_user_can_access_dashboard(
    dashboard_page: DashboardPage,
    test_app_url: str,
) -> None:
    """Verify that a saved authenticated session can access the dashboard."""

    # Navigate directly to the protected dashboard.
    dashboard_page.navigate(f"{test_app_url}/dashboard")

    # Verify that the protected page is available to the authenticated user.
    dashboard_page.assert_loaded()

    # Verify that the expected user information is displayed.
    dashboard_page.assert_welcome_message("Demo User")
