import requests
import json
import jmespath
import jsonschema
from purl import URL
from behave import when, given, then
from steps import parse_profile_var


@given('I am using site "{site}"')
def use_site(context, site):
    context.site = URL(site)


@given('I set "{header}" header to "{value}"')
@parse_profile_var
def set_header(context, header, value):
    context.headers[header] = value


@when('I send a GET request to "{server_endpoint}"')
@parse_profile_var
def send_get(context, server_endpoint):
    full_url = URL(context.site, path=server_endpoint)
    context.rest_response = requests.get(full_url, headers=context.headers)


@then('the response status should be "{response_status}"')
def get_status(context, response_status):
    status_code = context.rest_response.status_code
    assert (
        int(response_status) == status_code
    ), f"Assertion failed, {response_status} is different than {status_code}"


@then('the JSON at path "{jsonpath}" should be {value}')
def get_value_from_jsonpath(context, jsonpath, value):
    json_value = json.loads(value)
    json_response = json.loads(context.rest_response.text)
    json_path = jmespath.search(jsonpath, json_response)
    assert (
        json_path == json_value
    ), f"Assertion error: {json_path} of type {type(json_path)} is different than {json_value} of type {type(json_value)}"


@then('the JSON at path "{jsonpath}" should be')
def get_json_from_jsonpath(context, jsonpath):
    json_value = json.loads(context.text)
    json_response = json.loads(context.rest_response.text)
    json_path = jmespath.search(jsonpath, json_response)
    assert json_value == json_path, f"Assertion error: {json_value} is different than {json_path}"


@then('the JSON should be')
def get_json(context):
    json_value = json.loads(context.text)
    response_json = context.rest_response.json()
    assert json_value == response_json, f"Assertion error: {json_value} is different than {response_json}"


@then('the JSON has the following schema')
@then('the JSON has schema "{schema}"')
@parse_profile_var
def validate_schema(context, schema=''):
    if not schema:
        schema = json.loads(context.text)
    response_json = context.rest_response.json()
    json_schema = json.loads(schema)
    jsonschema.validate(response_json, json_schema)


@when('I send a POST request to "{server_endpoint}"')
@parse_profile_var
def send_get(context, server_endpoint=''):
    full_url = URL(context.site).add_path_segment(server_endpoint)
    headers = context.headers if context.headers else None
    body_msg = json.loads(context.text)
    context.rest_response = requests.post(full_url, json=body_msg, headers=headers)


@when('I store the JSON at path "{jsonpath}" into "{variable}"')
def get_value_from_jsonpath(context, jsonpath, variable):
    json_response = json.loads(context.rest_response.text)
    json_path = jmespath.search(jsonpath, json_response)
    context.profile[variable] = json_path
