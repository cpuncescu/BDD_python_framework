# BDD_python_framework
A python selenium web testing framework based on behave.
You can check the official behave documentation here: https://behave.readthedocs.io/en/latest/

The current framework is designed to be a _template_ and does not test any particular site. All the feature files, screenshots, videos and reports represent only a demo of what can be achieved using it.
The main purpose of implementing this framework was learning and trying different things therefore the lack of a proper Page Object Model or classic BDD approach is intentional.

**Note**

The chromedriver is installed in the same path as the python interpreter that I am using in pycharm(/usr/bin), therefore I can simply call the webdriver without specifying any path.
If you want to install it elsewhere, then you must specify the path when calling it.

**e.g:** driver = webdriver.Chrome(executable_path="path/to/chromedriver")

# Description

**Steps**

The steps are made to be as general as possible and accept parameters. They are defined in the files under the _steps_ folder.
Some of them have multiple definitions meaning that you can choose whichever definition of the same step, based on your targeted outcome.
They accept selectors as a tupple containing one of the method("NAME", "CSS", "XPATH", "ID", "CLASS", "TAG", "LINK_TEXT", PARTIAL_LINK_TEXT") and the actual locator.
e.g:
_Then I should see element "ID, password"_
_And I should see element "CSS, #username"_

**Selectors**

Selectors can be directly given when calling the step in the feature file(as stated above) or can be implemented in classes in a similar way as the Page Objects Model. This method is preferred as they are mapped to an alias which can be used accross multiple steps and feature files. If the selector is changed, than you modify it in a single place and then the change is automatically applied to every step where it is used.
They can be designed both to have parameters or not and you can call them with the same steps that we used previously but with the other step definition.
e.g:
_Then I should see "login_input(username)"_  - even if the same function: 'i_should_see' is used, you must call it differently  than the previous example.
_And I should see "logo_image()"_ - this selector does not take any parameter 
All the mapped selectors must be used with paranthesis, even if you do not design them that way. The rule is simple, if the selectors is not designed to have parameters, then you call them with empty paranthesis. If they need parameters, than you put them inside the paranthesis, separated by a comma.
The design and structure of the selectors does not represent the scope of this framework and it is totally up to you. The only thing which needs to be taken into account is that they must be structured under the **PageObjects** folder, where you currently have some examples.

**Multisteps**

The framework supports the execution of any sequence of the already defined steps.
This is useful where you have sequences of steps which repeat very often and help your tests to be more readable and less crowded.
They are designed in the multisteps folders and are just multiline strings which contain the desired steps.
This implementation serves as an alternative to the traditional BDD style, allowing for atomicity, reusability, and parameterization of steps. By doing so, it aims to eliminate duplicate code and provide greater flexibility in their usage.
Another advantage is that they can be implemented by juniors or testers who do not have programming skills.

**Profile**

The feature files are designed with a profile in mind.
Profiles are python dictionaries usually containing emails, passwords or other data needed for separating different users and access level.
Values stored or manipulated during the feature files are usually being stored in the current profile which should be declared in the begining of the test. Changing profiles during the same scenario is supported.

**REST API**

Testing the REST API is also supported.
It is recomended that the Headers and Authentification tokens should be set in the Background so that they can be used by each scenario from the feature file.

# DOCKER

In order to run tests with docker, you must have a docker client running in the background.

**Docker Compose**

You can set your docker configuration in the docker-compose-v3.yml file.
To run the tests using that configuration open a terminal, change the directory to the current project and then type: python3 docker_script.py --docker_compose=True
This will run all the tests, sequentiallty and will create a video containg all the scenarios.
You can find it in the Scenario_videos folder.

**Docker Parallel**

In order to have a scenario which you want to run in parallel, you must first add the @parallel tag to that scenario.
You can use the python3 docker_script.py --docker_parallel_video=True command to run the tests in parallel. This will initialize a selenium grid and video for each scenario. The tests will run in parallel and at the end, each scenario will have its own video in the Scenario_videos folder.
_I've tried to create a single Selenium grid and then nodes for each test but I ended up having videos which were empty and videos which contained multiple scenarios. For now, I will have each scenario with its own grid as it seems to work._

**Reports**

Work in progress, currently only a basic formatter is supported.
behave --format html --outfile path/to/report/reportname.html

# DISCLAIMER
This description does not contain all the functionality and design of the framework in detail.
The framework is subject to change, and might be updated frequently.
If you want something different or do not want all the changes, please fork the repo.
