@bdd
Feature: User login

  A user should be able to authenticate with valid credentials and receive
  clear feedback when the credentials are invalid or missing.

  @smoke
  Scenario: Successful login redirects to the dashboard
    Given I am on the login page
    When I log in with valid credentials
    Then I should be redirected to the dashboard

  Scenario: Invalid password is rejected
    Given I am on the login page
    When I log in with an invalid password
    Then I should see the login error "Invalid username or password"

  Scenario: Empty credentials are rejected
    Given I am on the login page
    When I submit empty credentials
    Then I should see the login error "Username and password are required"
