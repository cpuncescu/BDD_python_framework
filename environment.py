from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from environment import Configuration as cfg
from behave.model_core import Status
import os
import importlib


def get_classes():
    # create a set in order to ignore possible duplicate elements
    classes = set()
    """the path is relative to the 'tests' folder not the 'environment.py' file
    therefore we need to give it '../'"""
    for filename in os.listdir("../PageObjects"):
        if filename.endswith(".py") and filename != "__init__.py":
            module = importlib.import_module(f"PageObjects.{filename[:-3]}")
        for name, obj in module.__dict__.items():
            if isinstance(obj, type):
                classes.add(obj)
    assert len(classes) > 0, 'Assertion failed, there are no classes in your module'
    return list(classes)[0] if len(classes) == 1 else tuple(classes)


def before_all(context):
    context.driver = webdriver.Chrome()
    context.wait = WebDriverWait(context.driver, cfg.ELEMENT_WAIT_TIME)
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


def before_step(context, step):
    context.step = step


def before_scenario(context, scenario):
    context.profile = None
    context.scenario = scenario


def after_step(context, step):
    assert step.status == Status.passed, f"Step failed at line {step.line}"


def after_scenario(context, scenario):
    context.driver.execute_script("window.localStorage.clear();")
    if Status.failed:
        context.driver.save_screenshot(f"../failed_tests_screenshots/failed_{scenario}{scenario.tags[0]}.png")
