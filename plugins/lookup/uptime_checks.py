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
- hosts: localhost
  connection: local
  gather_facts: No
  vars:
    all_uptime_checks: "{{ lookup('ukcloud.pingdom.uptime_checks', api_token=<token>)}}"
  tasks:
  - name: Display details of all uptime checks
    debug:
      var: all_uptime_checks

# Get details of uptime checks tagged with "production"
- hosts: localhost
  connection: local
  gather_facts: No
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
    elements: dict
    contains:
        created:
            description: Unix epoch representation of when the uptime check was created.
            returned: always
            type: str
            sample: '1548851044'
        hostname:
            description: Domain name, including sub-domain, of the target for the uptime check.
            returned: always
            type: str
            sample: 'google.com'
        id:
            description: Unique identifier to the uptime check.
            returned: always
            type: str
            sample: '1234567'
        ipv6: false
            description: Whether the uptime check uses ipv6 instead of ipv4.
            returned: always
            type: str
            sample: 'false'
        lastdownend: 1615034565
            description: Unix epoch representation of the end of the last downtime period.
            returned: Only returned if the uptime check has ever been considered down.
            type: str
            sample: '1548851044'
        lastdownstart:
            description: Unix epoch representation of the start of the last downtime period.
            returned: Only returned if the uptime check has ever been considered down.
            type: str
            sample: '1548851044'
        lasterrortime:
            description: Unix epoch representation of when the uptime check last threw an error when it ran.
            returned: Only returned if the uptime check has ever thrown an error when run.
            type: str
            sample: '1615034507'
        lastresponsetime:
            description: Unix epoch representation of the uptime_check response time.
            returned: always
            type: str
            sample: '123'
        lasttesttime:
            description: Unix epoch representation of when the uptime check was last checked.
            returned: always
            type: str
            sample: '1615808445'
        maintenanceids:
            description: Ids of all maintenance windows which cover this uptime check.
            returned: Only returned if there are any maintenance windows which reference this uptime check.
            type: list
            elements: str
            sample:
                - '12345'
                - '67890'
        name:
            description: Name of the uptime check in Pingdom.
            returned: always
            type: str
            sample: 'Production host uptime check'
        probe_filters:
            description:
                - List of probe filters applied to the uptime check.
                - These limit geographically the uptime check is called from.
            returned: Only returned when probe filters are configured for the uptime check.
            type: list
            elements: str
            sample:
                - "region: EU"
        resolution:
            description: Frequency the uptime check will be run, in minutes.
            returned: always
            type: str
            sample: '5'
        status: up
            description: Whenther the uptime check is currently considered "up" or "down".
            returned: always
            type: str
            sample: 'down'
        type: http
            description: Protocol used by the uptime check, "http" or "https".
            returned: always
            type: str
            sample: 'https'
        verify_certificate: true
            description: Whether to consider the validity of the endpoints ssl certificate in the uptime check status.
            returned: always
            type: str
            sample: 'true'
"""


class LookupModule(LookupBase):
    """
    Ansible Lookup to get uptime check details from Pingdom
    """

    def run(self, terms, variables=None, **kwargs):
        """ main entrypoint for the lookup """
        display = Display()

        api_token = kwargs.get("api_token")
        if not api_token:
            raise AnsibleError(message="'api_token' must be passed to the ukcloud.pingdom.uptime_checks lookup.")
        tags = kwargs.get("tags")
        data = get_checks(api_token, tags)

        return [data]
