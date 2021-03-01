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
        required: true
        description:
            - The port which will be targeted
    encryption:
        required: true
        description:
            - Determine whether the connection is encrypted
    probe_filters:
        required: false
        description:
            - Filters used for probe selection
    shouldcontain:
        required: false
        description:
            - The target site should contain this string
    integrationids:
        required: false
        description:
            - The target site should contain this string
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
                "port": {"type": "str", "required": True},
                "encryption": {"type": "str", "required": True},
                "verify_certificate": {"type": "str", "required": False},
                "probe_filters": {"type": "str", "required": False},
                "shouldcontain": {"type": "str", "required": False},
                "integrationids": {"type": "int", "required": False},
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
        check_encryption = module.params['encryption']
        check_certificate = module.params['verify_certificate']
        check_filters = module.params['probe_filters']
        check_contain = module.params['shouldcontain']
        check_ids = module.params['integrationids']
        client = pingdompy.Client(apikey=api_key) 

        ## Logic allowing for checks to be paused on creation for testing purposes
        if module.params['pause'] == "y":
                check_pause = True
        else:
                check_pause = False

        ## Creates the check and returns the new checks id + name
        check = client.create_check({"host": check_url, "name": check_name, \
                "type": check_proto, "tags": check_tags, "resolution": check_timing, \
                "verify_certificate": check_certificate, "probe_filters": check_filters, \
                "shouldcontain": check_contain, "integrationids": check_ids, \
                "port": check_port, "encryption": check_encryption, "paused": check_pause})

        ## Returns verification to ansible
        module.exit_json(
                changed=True,
                response=check
        )

if __name__ == '__main__':
        main()
