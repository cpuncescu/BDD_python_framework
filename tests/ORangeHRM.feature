Feature: OrangeHRM Logo

  Background:
    When I navigate to "https://opensource-demo.orangehrmlive.com"

  @parallel_01
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

  @parallel_02
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


  @parallel_03
  @03
  Scenario: Login using multisteps
    Given profile "Admin"
    When I execute "login_action(${profile_username}, ${profile_password})"
    And I wait for 3 seconds
    When I press "user_dropdown()"
    And I take screenshot of "dashboard_menu()" and name it "dashboard_menu"
    And I press "logout()"


  @parallel_04
  @04
  Scenario: Login using javascript
    When I wait for 2 seconds
    And I execute javascript command "document.getElementsByName('username')[0].value='Admin'"
    And I execute javascript command "document.getElementsByName('password')[0].value='admin123'"
    And I execute javascript command "document.getElementsByClassName('oxd-form')[0].submit()"
    Then I should see "logo_image()"
    When I press "user_dropdown()"
    And I press "logout()"
