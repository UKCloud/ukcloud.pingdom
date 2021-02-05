#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.0'}

DOCUMENTATION = r'''
---
module: remove_maintenance
short_description: Delete a future maintenance window
description:
    - Deletes a maintenance window when given a specified ID
author: Jacob Gibbs (UKCloud Ltd)
options:
    apikey:
        required: true
        description:
            - Api key to auth with Pingdom
    maintenance_id:
        required: true
        description:
            - ID of the maintenance window to be deleted
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
        "maintenance_id": {"type": "str", "required": True},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=False)

    ## Assign params to more usable variables
    api_key = module.params['apikey']
    arg_maintenance_id = module.params['maintenance_id']
    client = pingdompy.Client(apikey=api_key) 

    delete = client.delete_maintenance(arg_maintenance_id)

    ## Return verification to ansible
    module.exit_json(
        changed=True,
        response=verify
    )

if __name__ == '__main__':
    main()