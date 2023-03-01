Feature: OrangeHRM Logo

  Background:
    When I navigate to "https://opensource-demo.orangehrmlive.com"

  @01
  Scenario: Logo Presence on OrangeHRM page
    Given profile "Admin"
    Then I should see "login_input(username)"
    And I should see "login_input(password)"
    When I fill "login_input(username)" with "${profile_username}"
    And I fill "login_input(password)" with "admin123"
    And I press "login_button()"
    Then I should see "logo_image()"
    And I should see "dashboard_item(Admin)"
    When I press "dashboard_item(Performance)"
    Then I should see "employee_review_page"
    When I press "user_dropdown()"
    And I press "logout()"

  @02
  Scenario Outline: Failed logins
    Then I should see "login_input(username)"
    And I should see "login_input(password)"
    When I fill "login_input(username)" with "<username>"
    And I fill "login_input(password)" with "<password>"
    Then I should see element "CLASS, orangehrm-login-error"
    When I press "login_button()"
    Examples:
      |username  |password
      |Admin     |admin1234
      |Admins    |admin1234
      |Admins    |admin123


  @03
  Scenario: Login using multisteps
    Given profile "Admin"
    When I execute "login_action(${profile_username}, ${profile_password})"
    And I wait for 3 seconds
    When I press "user_dropdown()"
    And I take screenshot of "dashboard_menu()" and name it "dashboard_menu"
    And I press "logout()"
