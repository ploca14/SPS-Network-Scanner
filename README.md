
# ARP Network Scanner

A python linux service for monitoring and finding unused IP address bindings

## Authors

- [@plocivoj](https://gitlab.fel.cvut.cz/plocivoj)
- [@svorcjak](https://gitlab.fel.cvut.cz/svorcjak)

## Installation

1. Clone this repo and cd into it
    - `$ git clone git@gitlab.fel.cvut.cz:plocivoj/arp-network-scanner.git`
    - `$ cd arp-network-scanner`
    - **Note: on Debian based systems you might need to install an addition package called python3.x-venv where x depends on your version of Python. You can check your Python version with `python3 --version`** This is a requirement for installation of a Python virtual environment.

2. Run our installation script as root `# ./install.sh`

3. Start the service
    - `# systemctl start arp-network-scanner`

4. Enable the service at boot (so it starts when the system starts)
    - `# systemctl enable arp-network-scanner`

You can now see if your service is running with: `# systemctl status arp-network-scanner`, or see its logs with `# journalctl -u arp-network-scanner`.
    
## Usage

1. Start the service and keep it running.

2. To list the unused IPs you can use the evaluation script with command `# evalarp` This command supports an option to select how old the listed data is. By default 2 weeks is used. Use `-d {number of days}`, to filter by days `-w {number of weeks}` to filter by weeks and `-m {number of months}` to filter by months. E.g. `# evalarp -d 2`. `# evalarp -a` can be used to list all records in the application.

## How it works

Once you start the service the Python script will constantly monitor all interfaces on a machine and on every ARP request it sees it will store the IP binding and timestamp to a small database. The `evalrp` command then evaluates the data in the database, showing you which IPs have not been used for a specified amount of time.

## Credits

The main idea of monitoring ARP traffic and keeping a database of IP bindings was our idea and we used the following sources to help us implement it.

- [Scapy ARP Monitor](https://scapy.readthedocs.io/en/latest/extending.html#more-examples:~:text=Here%20is%20another,from%20github.)
- [Python Linux Service](https://github.com/tal-zvon/python_linux_service)
