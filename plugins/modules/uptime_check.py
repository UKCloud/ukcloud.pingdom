#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = r'''
---
module: uptime_check
short_description: Create a new uptime check
description:
    - This will create an uptime check for a specified host
    - Once the check has been created, it will query the check and 
      output the created checks information to ansible as "check"
    - The pause option may be set to "y" to allow for checks to
      be created but instantly paused for testing purposes, otherwise
      this variable can be ommitted
author: Jacob Gibbs and Reiss Jarvis (UKCloud Ltd)
options:
    apikey:
        required: true
        type: string
        description:
            - The user's API key used to authorize the log in into Pingdom is taken as a string.
    uptimeid:
        required: false
        type: string
        description:
            - 
    host:
        required: false
        type: string
        description:
            - The host attribute contains the URL of the destination host which is being targeted by the uptime check. This attribute takes it's value as a string. (e.g. www.google.com).
    name:
        required: false
        type: string
        description:
            - A name must be given to identify the uptime check as a string. The name does not have to be unique.
    protocol:
        required: false
        type: string
        description:
            - The type of check taking place must be specified as a string (e.g. http, tcp, ping).
    tags:
        required: false
        type : string
        description:
            - Tags can be added to an uptime check to make them more organized and discoverable in the user interface. This attribute takes an array of strings where each tag must have a maximum length of 64 characters.
    timing:
        required: false
        type: string
        description:
            - The user can specify the number of minutes between each check. This attribute takes an integer, but defaults to 5 if not specified.
    port:
        required: false
        type: string
        description:
            - A specific port number can be targetted on the destination URL by setting setting the port number as an integer. 
    encryption:
        required: false
        type: string
        description:
            - The user can specify whether the uptime check uses encryption. This attribute takes a boolean (True or False), but defaults to False if not specified.
    verify_certificate:
        required: false
        type: string
        description:
            - An uptime check can treat the target site as down if it has an invalid or unverifiable certificate if the boolean verify_certificate attribute is set to True. If not specified, this attribute defaults to False.
    probe_filters:
        required: false
        type: string
        description:
            - The user can specify filters used for probe selection as an array of strings. Currently only region is supported (e.g. region:EU)
    shouldcontain:
        required: false
        type: string
        description:
            - The uptime check will only determine that the target site is up if it contains a specified string.
    integrationids:
        required: false
        type: string
        description:
            - The user can connect integrations which have been set up in the UI to the uptime check by specifying the integration IDs as a list of integers.
    url:
        required: false
        type: string
        description:
            - A path on the destination server can be set for the uptime check to target. This is taken as a string.
    pause:
        required: false
        type: string
        description:
            - This attribute takes a boolean (True/False). If set to True, the created uptime check will not automatically run immediately. If not specified, this attribute defaults to False.
notes:
    - More variables can be added following the above formatting and adding
      to the fields section within main
'''

######################
## 

import pingdompy
import datetime
from ansible.module_utils.basic import AnsibleModule

def create_new_check(module):
    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)
    ## Assign params to more usable variables
    api_key = module.params['apikey']
    check_host = module.params['host']
    check_name = module.params['name']
    check_proto = module.params['protocol']
    check_tags = module.params['tags']
    check_timing = module.params['timing']
    check_port = module.params['port']
    check_encryption = module.params['encryption']
    check_verification = module.params['verify_certificate']
    check_filters = module.params['probe_filters']
    check_contain = module.params['shouldcontain']
    check_ids = module.params['integrationids']
    check_url = module.params['url']
    check_pause = module.params['pause']
    client = pingdompy.Client(apikey=api_key) 
    ## Creates the check and returns the new checks id + name
    check = client.create_check({"host": check_host, "name": check_name, \
        "type": check_proto, "tags": check_tags, "resolution": check_timing, \
        "verify_certificate": check_verification, "probe_filters": check_filters, \
        "shouldcontain": check_contain, "integrationids": check_ids, "url": check_url, \
        "port": check_port, "encryption": check_encryption, "paused": check_pause})

    ## Find a way to check if it has changed.
    has_changed = True
    finish(has_changed, check)

def update_current_check(module, requested_id):
    module.params.pop("apikey")

    changes = {}
    for x in module.params:
        if module.params.get(x) != None:
            changes[x] = module.params.get(x)
        else:
            continue
    
    check = client.update_check(requested_id, changes)
    has_changed = isinstance(update, list)
    finish(has_changed, check)


def finish(has_changed, check):
            ## if update_check returns a list, then the update worked
    module.exit_json(
        changed = True,
        response = check
    )

def main():
        ## Set input variables
        fields = {
                "apikey": {"type": "str", "required": True, "no_log": True},
                "uptimeid": {"type": "str", "required": False},
                "host": {"type": "str", "required": False},
                "name": {"type": "str", "required": False},
                "protocol": {"type": "str", "required": False},
                "tags": {"type": "str", "required": False},
                "timing": {"type": "str", "required": False},
                "port": {"type": "str", "required": False},
                "encryption": {"type": "str", "required": False},
                "verify_certificate": {"type": "str", "required": False},
                "probe_filters": {"type": "str", "required": False},
                "shouldcontain": {"type": "str", "required": False},
                "integrationids": {"type": "str", "required": False},
                "url": {"type": "str", "required": False},
                "pause": {"type": "str", "required": False},
        }

        ###### Further variables could be added above and below to allow
        ###### for more complex checks to be added
        module = AnsibleModule(argument_spec=fields, supports_check_mode=False)

        requested_id = module.params.pop("uptimeid")
        api_key = module.params("apikey")
        uptime_name = module.params("uptimeid")
        does_exist = False

        client = pingdompy.Client(apikey=api_key)

        check_list = client.get_checks()["checks"]

        if requested_id:
            for x in check_list:
                if requested_id == check_list[x].id:
                    update_current_check(module, requested_id)
        elif uptime_name:
            for x in check_list:
                if uptime_name == check_list[x].name:
                    does_exist = True
                    update_current_check(module, requested_id)
            if does_exist == False:
                create_new_check(module)
            ## Return error that the user needs to include either an uptimeid or a name


if __name__ == '__main__':
        main()
