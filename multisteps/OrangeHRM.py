# e.g I execute "login_action(Admin, admin123)"
login_action = '''
    When I navigate to "https://opensource-demo.orangehrmlive.com"
    Then I should see "login_input(username)"
    And I should see "login_input(password)"
    When I fill "login_input(username)" with "{}"
    And I fill "login_input(password)" with "{}"
    And I press "login_button()"
    Then I should see "logo_image()"
    And I should see "dashboard_item(Admin)"
    '''