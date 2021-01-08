# Ansible Collection - ukcloud.pingdom

An Ansible Collection for managing SolarWinds Pingdom site monitoring. This collection has lookups for reading details from Pingdom as well as modules to create, modify and delete objects in Pingdom.

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

TBC

## Testing

TBC

## Contributing

TBC

## License

* GPL v3.0
