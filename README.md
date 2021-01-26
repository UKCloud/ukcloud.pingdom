# Ansible Collection - ukcloud.pingdom

An Ansible Collection for managing SolarWinds Pingdom site monitoring. This collection has lookups for reading details from Pingdom as well as modules to create, modify and delete objects in Pingdom.

## Pre-release

Note this repo is at a pre-release stage. Plugin names and parameters are likely to continue to change until this reaches the first major release 1.0.0

## Using this collection

Run `ansible-galaxy collection install git+https://github.com/UKCloud/ukcloud.pingdom` to install this collection.

This collection uses the python `pingdompy` library, the source can be found at [https://github.com/UKCloud/pingdompy](https://github.com/UKCloud/pingdompy). This library needs to be available to the python interpreter running Ansible. One way to do this is to use pip to install Ansible and the pingdompy library.

```bash
cd ~/code
git clone https://github.com/UKCloud/pingdompy.git
pip3 install ansible
pip3 install -e ~/code/pingdompy
```

## Modules

### uptime_check

This module is used to create a check from the given variables. Further variables can be implemented if required, for a full list, see [https://docs.pingdom.com/api/#tag/Checks/paths/~1checks/post](https://docs.pingdom.com/api/#tag/Checks/paths/~1checks/post) for a full list.

Required variable:
apikey - Api key for Pingdom

Optional variables currently implemented into the module:
url - Url of the host to check, eg www.google.com ('host' in the pingdom api docs)
name - The name of the check
protocol - The protocol used for the check, eg http,ping ('type' in the pingdom api docs)
tags - The tag(s) to add to the check, with each tag separated by a ',' if multiple
timing - The timing between the check running in minutes ('resolution' in pingdom api docs)
pause - Not Required. Can be set to "y" to pause the check on creation for testing

### maintenance_window

This module is used to create a maintenance window for a specified uptime id, or multiple uptime id's separated by a ','. See [https://docs.pingdom.com/api/#tag/Maintenance/paths/~1maintenance/post](https://docs.pingdom.com/api/#tag/Maintenance/paths/~1maintenance/post) for a complete list of potential variables.

This module requires the following variables to work:
apikey - Api key for Pingdom
uptimeid - Uptime id(s) for the required window. Multiple uptime id's separated with ','
name - The name for the maintenance window
start - The start time for the maintenance window in minutes from the current time
duration - The duration of the maintenance window in minutes

Once created, the module will verify that the maintenance window has been created and
output the window's information back to ansible.

### check_update

This module updates an existing check based on the parameters passed into it. It currently only supports updating a single check, and can only change the host and resolution of the check. For a list of potential variables to be implemented, see [https://docs.pingdom.com/api/#tag/Checks/paths/~1checks~1{checkid}/put](https://docs.pingdom.com/api/#tag/Checks/paths/~1checks~1{checkid}/put).

Requires the following variables:
apikey - Api key for pingdom
uptimeid - Uptime id of the check you want to update

Optional variables currently implemented into the module:
url - Url of the host you want to change the check to
timing - The timing between the check running in minutes

## Lookups

### uptime_checks

TBC

### maintenance_windows

TBC

## Development

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the default [`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

```bash
git clone git@github.com:UKCloud/ukcloud.pingdom.git ~/.ansible/collections/ansible_collections/ukcloud/pingdom
```

You can find more information in the [developer guide for collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## Testing

There are some basic testing playbooks in the /tests folder which exercise the uptime_check and maintenance_window modules. The playbooks require a Pingdom API key is passed in a variable called `vault_apikey`. Ansible Vault is one way to pass in this parameter.

The tests will create uptime checks and maintenance windows in Pingdom which will need to be manually deleted until `state: absent` is implemented in the modules.

See [here](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#testing-collections) also.

## Contributing

TBC

## License

* GPL v3.0
