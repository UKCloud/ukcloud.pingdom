""" Lookup to get details of Pingdom Uptime Checks
"""

from ansible.errors import AnsibleError, AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ansible_collections.ukcloud.pingdom.plugins.module_utils.pingdom_api \
    import get_checks


DOCUMENTATION = """
lookup: uptime_checks
author: Andrew Garner (agarner@ukcloud.com)
short_description: Lookup to get details of Pingdom Uptime Checks
description:
- Get details of uptime checks using the Pingdom API.
- The default Pingdom API version is 3.1 which is the only supported version by this plugin.
options:
    api_token:
        description: API token for authentication with Pingdom.
        required: True
        type: string
    tags:
        description: Comma-separated list of tags to filter the uptime checks returned.
        required: False
        type: string
"""

EXAMPLES = """
# Get details of all uptime checks
- hosts: all
  vars:
    all_uptime_checks: "{{ lookup('ukcloud.pingdom.uptime_checks', api_token=<token>)}}"
  tasks:
  - name: Display details of all uptime checks
    debug:
      var: all_uptime_checks

# Get details of uptime checks tagged with "production"
- hosts: all
  vars:
    tagged_uptime_checks: "{{ lookup('ukcloud.pingdom.uptime_checks', api_token=<token>, tags='production')}}"
  tasks:
  - name: Display details of production uptime checks
    debug:
      var: tagged_uptime_checks
"""

RETURN = """
checks:
   description: List of checks from Pingdom
   type: list
"""


class LookupModule(LookupBase):
    """
    Ansible Lookup to get uptime check details from Pingdom
    """

    def run(self, terms, variables=None, **kwargs):
        """ main entrypoint for the lookup """
        display = Display()
        display.debug(f"DEBUG: lookup uptime_checks called with terms = {terms}")
        display.debug(f"DEBUG: lookup uptime_checks called with kwargs = {kwargs}")

        api_token = kwargs.get("api_token")
        display.vvv(f"DEBUG: Got api_token of {api_token}")
        tags = kwargs.get("tags")
        display.vvv(f"DEBUG: Got tags of {tags}")
        if not api_token:
            raise AnsibleError(message="'api_token' must be passed to the ukcloud.pingdom.uptime_checks lookup.")
        data = get_checks(api_token, tags)

        return [data]
