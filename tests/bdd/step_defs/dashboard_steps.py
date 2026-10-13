from pytest_bdd import given, parsers, then

from pages.dashboard_page import DashboardPage


@given("I am an authenticated user on the dashboard")
def authenticated_user_opens_dashboard(
    dashboard_page: DashboardPage,
    test_app_url: str,
) -> None:
    """Open the protected dashboard with the existing authenticated fixture."""

    # dashboard_page is backed by the authenticated_page fixture, which
    # creates a fresh context using the saved authentication storage state.
    dashboard_page.navigate(f"{test_app_url}/dashboard")


@then("the dashboard title should be displayed")
def dashboard_title_should_be_displayed(
    dashboard_page: DashboardPage,
) -> None:
    """Verify the dashboard page title using the Page Object assertion."""

    # Keep title locators and assertions inside DashboardPage.
    dashboard_page.assert_loaded()


@then(parsers.parse('the dashboard should welcome "{username}"'))
def dashboard_should_welcome_user(
    dashboard_page: DashboardPage,
    username: str,
) -> None:
    """Verify the welcome message for the user named in the Gherkin step."""

    # Reuse the existing assertion rather than duplicating browser locators.
    dashboard_page.assert_welcome_message(username)
