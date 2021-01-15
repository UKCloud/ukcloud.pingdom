#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = r'''
---
module: check_update
short_description: Updates an existing check
description:
    - This module updates an existing check based on the parameters passed into it 
      (Does not support bulk changing)
    - Currently only works with the host and resolution of the check 
    - Currently only accepts updating the check with new value, not resetting to default
    - Returns the updated check and a confirmation message from the Pingdom Api as "response"
author: Jacob Gibbs (UKCloud Ltd)
options:
    apikey:
        required: true
        description:
            - Api key to auth with Pingdom
    uptimeid:
        required: true
        description:
            - Uptime id(s) for the check to be updated
    url:
        required: false
        description:
            - Url of the host to change to
    timing:
        required: false
        description:
            - The timing between the check running in minutes
notes:
    - Further variables can be added by adding them to "fields" and placing
      them in the "input_vars" dict by setting the key to the 
      variable name specified on the Pingdom API 
'''

######################

import pingdompy
import datetime
from ansible.module_utils.basic import AnsibleModule

def main():
    ## Set input variables
    fields = {
                "apikey": {"type": "str", "required": True, "no_log": True},
                "uptimeid": {"type": "str", "required": True},
                "url": {"type": "str", "required": False},
                "timing": {"type": "str", "required": False},
        }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)
    api_key = module.params['apikey']
    check = module.params['uptimeid']

    client = pingdompy.Client(apikey=api_key) 

    ## Dictionary of all possible inputs
    input_vars = {
        "host": module.params['url'],
        "resolution": module.params['timing'],
    }
    ## Logic to enable the change dictionary creation
    changes = {}
    for x in input_vars:
        if input_vars.get(x) != None:
            changes[x] = input_vars.get(x)
        else:
            continue

    update = client.update_check(check, changes)

    module.exit_json(
        changed=True,
        response=update
    )

if __name__ == '__main__':
    main()