### Description

A python linux service for monitoring and finding unused IP address bindings

### Install

1. Clone this repo and cd into it
    - `$ git clone git@gitlab.fel.cvut.cz:plocivoj/arp-network-scanner.git`
    - `$ cd arp-network-scanner`

2. Copy the python files to `/usr/local/lib`
    - `# mkdir /usr/local/lib/arp-network-scanner`
    - `# cp ./ /usr/local/lib/arp-network-scanner`
    - `# chown root:root /usr/local/lib/arp-network-scanner/service.py`
    - `# chmod 644 /usr/local/lib/arp-network-scanner/service.py`

3. Copy `arp-network-scanner.service` to `/etc/systemd/system/`
    - `# cp -v arp-network-scanner.service /etc/systemd/system/`
    - `# chown root:root /etc/systemd/system/arp-network-scanner.service`
    - `# chmod 644 /etc/systemd/system/arp-network-scanner.service`

4. Create virtual environment and install requirements into it
    - `$ cd /usr/local/lib/arp-network-scanner`
    - `$ python3 -m venv venv3`
    - `$ source venv3/bin/activate`
    - `$ pip install --upgrade pip`
    - `$ pip install -r requirements.txt`

5. Start the service
    - `# systemctl start arp-network-scanner`

6. Enable the service at boot (so it starts when the system starts)
    - `# systemctl enable arp-network-scanner`

You can now see if your service is running with: `# systemctl status arp-network-scanner`, or see its logs with `# journalctl -u arp-network-scanner`.

## Usage

1. Start the service and keep it running.

2. To list the unused IPs you can use the evaluation script with command `$ evaluate` This command supports an option to select how old the listed data is. By default 2 weeks is used. Use `-d {number of days}`, to filter by days `-w {number of weeks}` to filter by weeks and `-m {number of months}` to filter by months. E.g. `$ evaluate -d 2`. `evaluate -a` can be used to list all records in the application.