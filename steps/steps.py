from selenium.webdriver.support import expected_conditions as EC
from behave import when, given, then
from environment import Profiles
from environment import Configuration as cfg
import time
import re


def extract_params(pageobject):
    match = re.search(r"\((.*?)\)", pageobject)
    if match:
        return match.group(1)
    else:
        return ""


def page_object_selector(context, pageobject):
    # get the parameters inside the '()' if any
    params = extract_params(pageobject)
    final_attribute = pageobject.split("(")[0]
    """create a class which inherits the attributes from all of
    the existing classes of the PageObjects folder"""

    class PageObj(*context.pageObjClasses):
        def __init__(self, *args):
            for cls in context.pageObjClasses:
                cls.__init__(self, *args)

    Obj = PageObj(params)
    """returns a tuple of format (METHOD, locator)
    e.g ('Name', 'password')"""
    selector = getattr(Obj, final_attribute)
    return selector


def return_selector_method(context, selector, pageobject):
    if pageobject:
        method, locator = page_object_selector(context, pageobject)
    elif selector:
        method, locator = selector.split(",", maxsplit=1)
    else:
        assert False, "No selector or page object given"
    return context.locate_method[method], locator.strip()


def parse_profile_var(func):
    def wrapper(context, *args, **kwargs):
        for kwname, arg in kwargs.items():
            """takes all the variable names with format ${var_name}
            and returns a list with variable name/s: ['var_name']"""
            matches = re.findall(r"\${(.*?)}", arg)
            values = []
            if matches:
                for i in matches:
                    assert (
                        i in context.profile
                    ), f"{i} is not found in the profile variables"
                    """takes the name of the variable and replaces it with
                    the value stored in the profile then adds it to a list"""
                    values.append(context.profile[i])
                new_arg = re.sub(r"\$\{(\w+)\}", "{}", arg)
                """replaces the variables with the actual values
                then returns the parameter to the function
                """
                kwargs[kwname] = new_arg.format(*values)
        return func(context, *args, **kwargs)

    return wrapper


@given('profile "{profile}"')
def load_profile(context, profile):
    assert profile in Profiles.Profiles, f"There is no profile {profile} defined"
    context.profile = Profiles.Profiles[profile]


@when('I navigate to "{url}"')
def navigate_to(context, url):
    context.driver.get(url)
    current_url = context.driver.current_url
    assert url in current_url, f"Assertion failed, the current url is {current_url}"


@when("I wait for {seconds:d} seconds")
def wait_for(context, seconds):
    time.sleep(seconds)


@then('I should see "{pageobject}"')
@then('I should see element "{selector}"')
def i_should_see(context, selector="", pageobject=""):
    method, locator = return_selector_method(context, selector, pageobject)
    element = context.wait.until(
        EC.visibility_of_all_elements_located((method, locator))
    )
    assert len(element) == 1, f"Found more than 1 element: {len(element)}"
    return element[0]


@when('I press "{pageobject}"')
@when('I press on "{selector}"')
@parse_profile_var
def i_press(context, selector="", pageobject=""):
    element = i_should_see(context, selector, pageobject)
    clickable_element = context.wait.until(EC.element_to_be_clickable(element))
    clickable_element.click()


@when('I fill "{pageobject}" with "{text}"')
@when('I fill selector "{selector}" with "{text}"')
@parse_profile_var
def i_fill(context, text, selector="", pageobject=""):
    element = i_should_see(context, selector, pageobject)
    clickable_element = context.wait.until(EC.element_to_be_clickable(element))
    clickable_element.clear()
    clickable_element.send_keys(text)


@when('I execute "{step}"')
def i_execute(context, step):
    parameters = [x.strip() for x in extract_params(step).split(",")]
    func = context.multisteps[step.split("(")[0]]
    final_steps = func.format(*parameters) if parameters else func
    param_nr = func.count("{}")
    assert param_nr == len(
        parameters
    ), f"You passed {len(parameters)} parameters but the multisteps need {param_nr}"
    context.execute_steps(final_steps)


@when('I take screenshot of "{pageobject}" and name it "{screenshot_name}"')
@when('I take screenshot of element "{selector}" and name it "{screenshot_name}"')
def i_take_screenshot(context, screenshot_name, selector="", pageobject=""):
    element = i_should_see(context, selector, pageobject)
    element.screenshot(f"../screenshots/{screenshot_name}.png")


@when('I drag element "{pageobject_source}" over "{page_object_dest}"')
@when('I drag selector "{selector_source}" over "{selector_dest}"')
def i_drag_drop(
    context,
    selector_source="",
    selector_dest="",
    pageobject_source="",
    page_object_dest="",
):
    source_elem = i_should_see(context, selector_source, pageobject_source)
    dest_elem = i_should_see(context, selector_dest, page_object_dest)
    context.AC.drag_and_drop(source_elem, dest_elem).perform()
