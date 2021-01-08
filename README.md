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

TBC

### maintenance_window

TBC

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

See [here](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#testing-collections).

## Contributing

TBC

## License

* GPL v3.0
