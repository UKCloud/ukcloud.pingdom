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
    host:
        required: false
        description:
            - Url of the host to change to
    resolution:
        required: false
        description:
            - The timing between the check running in minutes
notes:
    - Future variables can be added by using their specified pingdom api names and adding
      them to the options and fields section.
'''

######################
import pingdompy
from ansible.module_utils.basic import AnsibleModule

def main():
    ## Set input variables
    fields = {
                "apikey": {"type": "str", "required": True, "no_log": True},
                "uptimeid": {"type": "str", "required": True},
                "host": {"type": "str", "required": False},
                "resolution": {"type": "str", "required": False},
        }
    
    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)
    ## Removes keys Pingdom won't accept from the dict
    api_key = module.params.pop("apikey")
    check = module.params.pop("uptimeid")

    client = pingdompy.Client(apikey=api_key) 

    ## Logic to enable the change dictionary creation
    changes = {}
    for x in module.params:
        if module.params.get(x) != None:
            changes[x] = module.params.get(x)
        else:
            continue
    ## Creates the update and returns an output dependant message
    update = client.update_check(check, changes)
    ## Sends response back upto ansible
    module.exit_json(
        changed = isinstance(update, list),
        response = update
    )

if __name__ == '__main__':
    main()