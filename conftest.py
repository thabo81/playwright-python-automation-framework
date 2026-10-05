import json
from collections.abc import Generator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def test_app_url() -> Generator[str, None, None]:
    """Serve deterministic local test data for UI and API tests."""
    assets_dir = Path(__file__).parent / "tests" / "assets"

    class TestHandler(BaseHTTPRequestHandler):
        def _send_file(self, filename: str, content_type: str) -> None:
            """Send a local HTML asset to the browser."""
            content = (assets_dir / filename).read_bytes()

            # Return a successful HTTP response.
            self.send_response(200)

            # Tell the browser what type of content it is receiving.
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()

            # Write the file contents to the response body.
            self.wfile.write(content)

        def do_GET(self) -> None:
            """Handle browser GET requests for the demo application."""
            if self.path == "/api/user":
                # Return deterministic JSON data for API tests.
                body = json.dumps(
                    {"id": 1, "name": "Demo User", "role": "SDET"}
                ).encode()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path in {"/", "/index.html"}:
                # Serve the original home page.
                self._send_file("index.html", "text/html; charset=utf-8")
                return

            if self.path == "/login":
                # Serve the login page.
                self._send_file("login.html", "text/html; charset=utf-8")
                return

            if self.path == "/dashboard":
                # Only authenticated users should be allowed to view
                # the dashboard.
                if "auth=authenticated" not in self.headers.get("Cookie", ""):
                    self.send_response(302)
                    self.send_header("Location", "/login")
                    self.end_headers()
                    return

                self._send_file(
                    "dashboard.html",
                    "text/html; charset=utf-8",
                )
                return

            self.send_response(404)
            self.end_headers()

        def do_POST(self) -> None:
            """Handle API requests that change application state."""
            if self.path != "/api/login":
                self.send_response(404)
                self.end_headers()
                return

            # Read the JSON request body sent by the login page.
            content_length = int(self.headers.get("Content-Length", "0"))
            request_body = self.rfile.read(content_length)

            try:
                credentials = json.loads(request_body)
            except json.JSONDecodeError:
                credentials = {}

            username = credentials.get("username", "")
            password = credentials.get("password", "")

            if not username or not password:
                self.send_response(400)
                body = json.dumps(
                    {"detail": "Username and password are required"}
                ).encode()
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if username == "testuser" and password == "Password123":
                # Set a simple session cookie to represent a successful login.
                body = json.dumps({"message": "Login successful"}).encode()

                self.send_response(200)
                self.send_header("Set-Cookie", "auth=authenticated; Path=/")
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            # Reject credentials that do not match the known test account.
            self.send_response(401)
            body = json.dumps(
                {"detail": "Invalid username or password"}
            ).encode()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            """Keep the local test server output quiet."""
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), TestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        # Stop the test server after the entire test session completes.
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Create a HomePage object for the current test."""
    # Pytest provides the Playwright Page fixture.
    # We wrap that page in our HomePage Page Object.
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Create a LoginPage object for the current test."""
    # Reuse the browser page that Pytest created and wrap it
    # with the LoginPage Page Object.
    return LoginPage(page)


@pytest.fixture(scope="session")
def authenticated_storage_state(
    browser,
    test_app_url: str,
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Create and persist authenticated browser state for the test session."""
    # Store the authentication state outside the repository working tree
    # so session credentials are never accidentally committed.
    state_directory = tmp_path_factory.mktemp("playwright-auth")
    state_path = state_directory / "auth_state.json"

    # Create an isolated browser context used only to establish authentication.
    context = browser.new_context()
    page = context.new_page()

    try:
        # Open the application's login page.
        page.goto(f"{test_app_url}/login")

        # Fill in the known valid test credentials.
        page.get_by_label("Username").fill("testuser")
        page.get_by_label("Password").fill("Password123")

        # Submit the login form and wait for the dashboard.
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/dashboard")

        # Save cookies/local storage so later tests can reuse the session.
        context.storage_state(path=state_path)
    finally:
        # Always close the temporary authentication context.
        context.close()

    return state_path


@pytest.fixture
def authenticated_page(
    browser,
    authenticated_storage_state: Path,
) -> Generator[Page, None, None]:
    """Create a browser page using the saved authenticated state."""
    # Create a fresh context from the previously saved authentication state.
    context = browser.new_context(
        storage_state=authenticated_storage_state,
    )
    page = context.new_page()

    try:
        # Give the test a fully configured authenticated page.
        yield page
    finally:
        # Close the context after the test to keep tests isolated.
        context.close()


@pytest.fixture
def dashboard_page(authenticated_page: Page) -> DashboardPage:
    """Create a DashboardPage object using an authenticated page."""
    # Wrap the authenticated Playwright page in the Dashboard Page Object.
    return DashboardPage(authenticated_page)
