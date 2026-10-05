import json
from collections.abc import Generator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import Page

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
