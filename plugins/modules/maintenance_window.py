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
import time
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
    ## Assign params to more usable variables
    api_key = module.params['apikey']
    maint_name = module.params['name']
    start_time = module.params['start']
    duration_time = module.params['duration']
    arg_uptimeid = module.params['uptimeid']

    client = pingdompy.Client(apikey=api_key) 
    ## Calculates the start and end times for the window                      
    start = datetime.datetime.now() + datetime.timedelta(minutes=int(start_time))
    end = start + datetime.timedelta(minutes=int(duration_time))

    ## Creates window and converts times to something pingdom accepts
    window = client.create_maintenance({"description": maint_name, \
            "from": int(time.mktime(start.timetuple())), "to": int(time.mktime(end.timetuple())), "uptimeids": arg_uptimeid})

    ## Verification of window creation
    verify = client.get_maintenance(window['id'])

    ## Return verification to ansible
    module.exit_json(
        changed=True,
        response=verify
    )

    ###### The times returned to ansible are in unix time, something could
    ###### be implemented to make this more human readable

if __name__ == '__main__':
    main()