from pytest_bdd import given, parsers, then, when

from pages.login_page import LoginPage


@given("I am on the login page")
def user_is_on_login_page(
    login_page: LoginPage,
    test_app_url: str,
) -> None:
    """Open the login page through the existing Page Object."""

    # Reuse LoginPage instead of putting Playwright selectors
    # directly into the Gherkin step definition.
    login_page.open(test_app_url)


@when("I log in with valid credentials")
def user_logs_in_with_valid_credentials(
    login_page: LoginPage,
) -> None:
    """Submit the known valid test credentials."""

    # Keep the interaction in the Page Object so Gherkin steps
    # describe behaviour rather than selector implementation.
    login_page.login("testuser", "Password123")


@when(
    parsers.re(
        r'I attempt to log in with username "(?P<username>.*?)" '
        r'and password "(?P<password>.*?)"'
    )
)
def user_attempts_login_with_credentials(
    login_page: LoginPage,
    username: str,
    password: str,
) -> None:
    """Submit credentials supplied by the Scenario Outline Examples."""

    # A non-greedy regex also accepts empty strings for negative test data,
    # allowing the empty-credentials row to exercise required-field checks.
    login_page.login(username, password)


@then("I should be redirected to the dashboard")
def user_should_reach_dashboard(
    login_page: LoginPage,
) -> None:
    """Verify that successful authentication reaches the dashboard."""

    # Wait for navigation rather than relying on an arbitrary sleep.
    login_page.page.wait_for_url("**/dashboard")

    # Confirm the browser ended on the expected route.
    assert login_page.page.url.endswith("/dashboard")


@then(parsers.parse('I should see the login error "{expected_message}"'))
def user_should_see_login_error(
    login_page: LoginPage,
    expected_message: str,
) -> None:
    """Verify the expected error text for a rejected login attempt."""

    # Reuse the Page Object assertion for both negative examples.
    login_page.assert_login_error(expected_message)
