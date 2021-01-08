#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible.errors import AnsibleError
from ansible.module_utils.urls import open_url
from ansible.utils.display import Display


display = Display()
rest_success_matrix = {'GET': [200],
                       'PUT': [200, 204],
                       'POST': [200, 201],
                       'DELETE': [200, 204]}

PINDGOM_API_URL = "https://api.pingdom.com/api/3.1"
CHECKS_URL = f"{PINDGOM_API_URL}/checks"

def call_url(module, method, url, data=None, headers=None,
             force_basic_auth=False):
    """ Lightweight wrapper around Ansible's open_url module_utils method.

    This method checks the http status code returned and raises an AnsibleError
    if the REST method and response code indicate failure.

    Args:
        force_basic_auth:
        headers:
        data:
        module (AnsibleModule):
        method (str): REST method to use, one of GET, PUT, POST, DELETE
        url (str): url to call which will be appended to module.params['url']

    Returns:
        (HTTPResponse): On success returns an HTTPResponse object. Success is
            determined by the response code and the HTTP method called.

    Raises:
        (AnsibleError):
    """
    url = module.params['url'] + url

    # See https://github.com/ansible/ansible/blob/devel/lib/ansible/module_utils/urls.py#L1083
    # Returns an HTTPResponse, see https://docs.python.org/3/library/http.client.html#httpresponse-objects
    response = open_url(url=url, url_username=module.params['username'],
                        url_password=module.params['password'],
                        data=data, headers=headers, method=method,
                        force_basic_auth=force_basic_auth)
    http_status = response.getcode()
    display.debug("Got response code from Pingdom of " + str(http_status))
    if http_status not in rest_success_matrix[method]:
        raise AnsibleError()

    return response.read()


def create_bearer_token_header(api_token):
    headers = {'Authorization': f'Bearer {api_token}'}
    return headers


def get_checks(api_token, tags):
    headers = create_bearer_token_header(api_token)
    display.debug(f"DEBUG: Calling url {CHECKS_URL}")
    if tags:
        url = f"{CHECKS_URL}?tags={tags}"
    else:
        url = CHECKS_URL
    response = open_url(url=url, headers=headers,
                        method="GET", force_basic_auth=True)
    http_status = response.getcode()
    display.debug("Got response code from Pingdom of " + str(http_status))
    if http_status not in rest_success_matrix["GET"]:
        raise AnsibleError()

    # Convert bytes response to a string before returning
    data = response.read()
    return str(data, 'utf-8')
