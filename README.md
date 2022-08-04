### Description

A python linux service for monitoring and finding unused IP address bindings

### Install

1. Clone this repo and cd into it
    - `$ git clone git@gitlab.fel.cvut.cz:plocivoj/arp-network-scanner.git`
    - `$ cd arp-network-scanner`

2. Run our installation script as root `# ./install.sh`

3. Start the service
    - `# systemctl start arp-network-scanner`

4. Enable the service at boot (so it starts when the system starts)
    - `# systemctl enable arp-network-scanner`

You can now see if your service is running with: `# systemctl status arp-network-scanner`, or see its logs with `# journalctl -u arp-network-scanner`.

## Usage

1. Start the service and keep it running.

2. To list the unused IPs you can use the evaluation script with command `$ evaluate` This command supports an option to select how old the listed data is. By default 2 weeks is used. Use `-d {number of days}`, to filter by days `-w {number of weeks}` to filter by weeks and `-m {number of months}` to filter by months. E.g. `$ evaluate -d 2`. `evaluate -a` can be used to list all records in the application.