Feature: Misc practice

  Background:
    When I navigate to "https://testautomationpractice.blogspot.com/"

  @A1
  Scenario: Drag and drop
    Given profile "Admin"
    When I drag element "drag_source()" over "drop_source()"