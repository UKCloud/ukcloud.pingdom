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
author: Jacob Gibbs (UKCloud Ltd)
options:
    apikey:
        required: true
        description:
            - api key to auth with Pingdom
    url:
        required: true
        description:
            - Url of the host to check, eg www.google.com
    name:
        required: true
        description:
            - Name of the check
    protocol:
        required: true
        description:
            - The protocol used for the check, eg http, ping etc
    tags:
        required: true
        description:
            - The tag(s) to add to the check separated with ,
    timing:
        required: true
        description:
            - The timing between the check running in minutes
   port:
        required: false
        description:
            - The timing between the check running in minutes
    pause:
        required: false
        description:
            - Not Required. Please set to "y" to pause the check on creation for testing
notes:
    - More variables can be added following the above formatting and adding
      to the fields section within main
'''

######################

import pingdompy
import datetime
from ansible.module_utils.basic import AnsibleModule

def main():
        ## Set input variables
        fields = {
                "apikey": {"type": "str", "required": True, "no_log": True},
                "url": {"type": "str", "required": True},
                "name": {"type": "str", "required": True},
                "protocol": {"type": "str", "required": True},
                "tags": {"type": "str", "required": True},
                "timing": {"type": "str", "required": True},
                "port": {"type": "str", "required": False},
                "pause": {"type": "str", "required": False},
        }

        ###### Further variables could be added above and below to allow
        ###### for more complex checks to be added

        module = AnsibleModule(argument_spec=fields, supports_check_mode=False)
        ## Assign params to more usable variables
        api_key = module.params['apikey']
        check_url = module.params['url']
        check_name = module.params['name']
        check_proto = module.params['protocol']
        check_tags = module.params['tags']
        check_timing = module.params['timing']
        check_port = module.params['port']
        client = pingdompy.Client(apikey=api_key) 

        ## Logic allowing for checks to be paused on creation for testing purposes
        if module.params['pause'] == "y":
                check_pause = True
        else:
                check_pause = False

        ## Creates the check and returns the new checks id + name
        check = client.create_check({"host": check_url, "name": check_name, \
                "type": check_proto, "tags": check_tags, "resolution": check_timing, \
                "port": check_port, "paused": check_pause})

        ## Returns verification to ansible
        module.exit_json(
                changed=True,
                response=check
        )

if __name__ == '__main__':
        main()