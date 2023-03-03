from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from environment import Configuration as cfg
from behave.model_core import Status
import os
import importlib


def get_classes():
    # create a set in order to ignore possible duplicate elements
    classes = set()
    """the path is relative to the 'tests' folder not the 'environment.py' file
    therefore we need to give it '../'"""
    for root, dirs, files in os.walk("../PageObjects"):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                """
                os.path.join(root, filename) will return a relative path to the file
                e.g ../PageObjects/OrangeHRM/DashboardMenu.py
                for the importlib we need the format: PageObjects.OrangeHRM.DashboardMenu
                """
                module_path = os.path.join(root, filename)[:-3].replace("/", ".")
                module_path = module_path.split("...")[-1]

                module = importlib.import_module(module_path)
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        classes.add(obj)
    assert len(classes) > 0, "Assertion failed, there are no classes in your module"
    return list(classes)[0] if len(classes) == 1 else tuple(classes)

def get_multisteps():
    config_dict = {}

    # loop through the files in the multisteps directory
    for filename in os.listdir("../multisteps"):
        # check if the file is a Python module
        if filename.endswith('.py') and filename != '__init__.py':
            # import the module dynamically
            module_name = filename[:-3]
            module = importlib.import_module(f'multisteps.{module_name}')

            # add the module's variables to the dictionary
            for name, value in module.__dict__.items():
                # exclude built-in names and private names
                if not name.startswith('__') and not callable(value):
                    config_dict[name] = value
    return config_dict


def before_all(context):
    context.driver = webdriver.Chrome()
    context.wait = WebDriverWait(context.driver, cfg.ELEMENT_WAIT_TIME)
    context.AC = ActionChains(context.driver)
    context.locate_method = {
        "NAME": By.NAME,
        "CSS": By.CSS_SELECTOR,
        "XPATH": By.XPATH,
        "ID": By.ID,
        "CLASS": By.CLASS_NAME,
        "TAG": By.TAG_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
    }
    context.pageObjClasses = get_classes()
    context.multisteps = get_multisteps()


def before_step(context, step):
    context.step = step


def before_scenario(context, scenario):
    context.profile = None
    context.scenario = scenario


def after_step(context, step):
    assert step.status == Status.passed, f"Step failed at line {step.line}"


def after_scenario(context, scenario):
    context.driver.execute_script("window.localStorage.clear();")
    if context.step.status == Status.failed:
        context.driver.save_screenshot(
            f"../failed_tests_screenshots/failed_{scenario}{scenario.tags[0]}.png"
        )
        print(f"Step failed at line {context.step.line}")
