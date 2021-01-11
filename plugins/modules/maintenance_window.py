#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = r'''
---
module: maintenance_window
short_description: create a maintenance window for a check
description:
    - Creates a maintenance window for a specified uptime id based on inputs
    - Only accepts uptime id's, no names/tags
    - Verifies maintenance windows has been created and returns the output 
       of this check in the variable "verify" to ansible
author: Jacob Gibbs (UKCloud Ltd)
options:
    apikey:
        required: true
        description:
            - Api key to auth with Pingdom
    uptimeid:
        required: true
        description:
            - Uptime id(s) to create a maintenance window for. Separated with ,
    name:
        required: true
        description:
            - Name for the maintenance window
    start:
        required: true
        description:
            - Start time of maintenance in minutes from the current time
    duration:
        required: true
        description:
            - Duration of the maintenance in minutes
notes:
    - When successful, will return the information of the window created 
      and will be displayed by ansible
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
        "name": {"type": "str", "required": True},
        "start": {"type": "str", "required": True},
        "duration": {"type": "str", "required": True},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)
    api_key = module.params['apikey']
    maint_name = module.params['name']
    start_time = module.params['start']
    duration_time = module.params['duration']
    arg_uptimeid = module.params['uptimeid']

    ## This is set to false to disable the ability 
    ## to search via check name/tag
    checks = False

    #### Creating window
    client = pingdompy.Client(apikey=api_key)                       
    start = datetime.datetime.now() + datetime.timedelta(minutes=int(start_time))
    end = start + datetime.timedelta(minutes=int(duration_time))
    window = client.create_maintenance({"checks": checks, "name": maint_name, \
            "start": start, "stop": end, "uptime_ids": arg_uptimeid})

    ## Verification of window creation
    verify = client.get_maintenance(window._id)

    ## Return verification to ansible
    module.exit_json(
        changed=True,
        response=verify
    )

if __name__ == '__main__':
    main()