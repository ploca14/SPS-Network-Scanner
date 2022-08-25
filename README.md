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

5. You can uninstall the program by running the uninstallation script.
    - `# ./uninstall.sh`

You can now see if your service is running with: `# systemctl status arp-network-scanner`, or see its logs with `# journalctl -u arp-network-scanner`.
    
## Usage

1. Start the service and keep it running.

2. To list the unused IPs you can use the evaluation script with command `# evalarp` This command supports an option to select how old the listed data is. By default 2 weeks is used. Use `-h {number of hours}` `-d {number of days}`, to filter by days `-w {number of weeks}` to filter by weeks and `-m {number of months}` to filter by months. E.g. `# evalarp -d 2`. `# evalarp -a` can be used to list all records in the application.

3. You can list never seen IPs in your networks by issuing `# evalarp -n` command.

*Note: this program only scans active ethernet interfaces named either eth# or enp0s#*

## How it works

Once you start the service the Python script will constantly monitor all interfaces on a machine and on every ARP request it sees it will store the IP binding and timestamp to a small database. The `evalrp` command then evaluates the data in the database, showing you which IPs have not been used for a specified amount of time.

## Credits

The main idea of monitoring ARP traffic and keeping a database of IP bindings was our idea and we used the following sources to help us implement it.

- [Scapy ARP Monitor](https://scapy.readthedocs.io/en/latest/extending.html#more-examples:~:text=Here%20is%20another,from%20github.)
- [Python Linux Service](https://github.com/tal-zvon/python_linux_service)
