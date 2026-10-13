@bdd
Feature: User login

  A user should be able to authenticate with valid credentials and receive
  clear feedback when the credentials are invalid or missing.

  Background:
    Given I am on the login page

  @smoke
  Scenario: Successful login redirects to the dashboard
    When I log in with valid credentials
    Then I should be redirected to the dashboard

  @negative
  Scenario Outline: Login rejects invalid credentials
    When I attempt to log in with username "<username>" and password "<password>"
    Then I should see the login error "<expected_message>"

    Examples:
      | case               | username | password      | expected_message                    |
      | Invalid password   | testuser | WrongPassword | Invalid username or password       |
      | Empty credentials  |          |               | Username and password are required |
