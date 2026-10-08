from pytest_bdd import given, then, when

from pages.login_page import LoginPage


@given("I am on the login page")
def user_is_on_login_page(
    login_page: LoginPage,
    test_app_url: str,
) -> None:
    """Open the login page through the existing Page Object."""

    # Reuse the LoginPage abstraction instead of putting
    # Playwright selectors directly into the Gherkin step.
    login_page.open(test_app_url)


@when("I log in with valid credentials")
def user_logs_in_with_valid_credentials(
    login_page: LoginPage,
) -> None:
    """Submit the known valid test credentials."""

    # Keep the interaction inside the Page Object so the BDD layer
    # describes behaviour rather than implementation details.
    login_page.login("testuser", "Password123")


@then("I should be redirected to the dashboard")
def user_should_reach_dashboard(
    login_page: LoginPage,
) -> None:
    """Verify that successful authentication reaches the dashboard."""

    # Wait for the application redirect before asserting the final URL.
    login_page.page.wait_for_url("**/dashboard")

    # Confirm that the browser finished on the dashboard route.
    assert login_page.page.url.endswith("/dashboard")
