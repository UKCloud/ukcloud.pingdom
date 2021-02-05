#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = r'''
---
module: remove_check
short_description: Delete a specified check
description:
    - Deletes a check when given a specified ID
    - Only deletes one at a time
author: Jacob Gibbs (UKCloud Ltd)
options:
    apikey:
        required: true
        description:
            - Api key to auth with Pingdom
    uptimeid:
        required: true
        description:
            - Uptime id of the check to delete
notes:
    - When successful, a confirmation that the delete occured will be passed back
      to ansible
'''

######################

import pingdompy
from ansible.module_utils.basic import AnsibleModule

def main():
    ## Set input variables
    fields = {
        "apikey": {"type": "str", "required": True, "no_log": True},
        "uptimeid": {"type": "str", "required": True},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)

    ## Assign params to more usable variables
    api_key = module.params['apikey']
    arg_uptimeid = module.params['uptimeid']
    client = pingdompy.Client(apikey=api_key) 

    delete = client.delete_check(arg_uptimeid)

    ## Return verification to ansible
    module.exit_json(
        changed=True,
        response=verify
    )

if __name__ == '__main__':
    main()