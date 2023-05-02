import requests
import json
import jmespath
from purl import URL
from behave import when, given, then
from environment import Profiles


@given('I am using site "{site}"')
def use_site(context, site):
    context.site = URL(site)


@given('I set "{header}" header to "{value}"')
def set_header(context, header, value):
    context.headers[header] = value


@when('I send a GET request to ""')
@when('I send a GET request to "{server_endpoint}"')
def send_get(context, server_endpoint=""):
    full_url = URL(context.site).add_path_segment(server_endpoint)
    context.rest_response = requests.get(full_url)


@then('the response status should be "{response_status}"')
def get_status(context, response_status):
    status_code = context.rest_response.status_code
    assert (
        int(response_status) == status_code
    ), f"Assertion failed, {response_status} is different than {status_code}"


@then('the JSON at path "{jsonpath}" should be {value}')
def get_status(context, jsonpath, value):
    json_value = json.loads(value)
    json_response = json.loads(context.rest_response.text)
    json_path = jmespath.search(jsonpath, json_response)
    assert (
        json_path == json_value
    ), f"Assertion error: {json_path} of type {type(json_path)} is different than {json_value} of type {type(json_value)}"
