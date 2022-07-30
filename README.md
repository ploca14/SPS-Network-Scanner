### Description

A python linux service for monitoring and finding unused IP address bindings

### Install

1. Clone this repo and cd into it
    - `git clone git@gitlab.fel.cvut.cz:plocivoj/arp-network-scanner.git`
    - `cd arp-network-scanner`

2. Copy the python files to `/usr/local/lib`
    - `sudo mkdir /usr/local/lib/arp-network-scanner`
    - `sudo cp ./ /usr/local/lib/arp-network-scanner`
    - `sudo chown root:root /usr/local/lib/arp-network-scanner/service.py`
    - `sudo chmod 644 /usr/local/lib/arp-network-scanner/service.py`

3. Copy `arp-network-scanner.service` to `/etc/systemd/system/`
    - `sudo cp -v arp-network-scanner.service /etc/systemd/system/`
    - `sudo chown root:root /etc/systemd/system/arp-network-scanner.service`
    - `sudo chmod 644 /etc/systemd/system/arp-network-scanner.service`

4. Create virtual environment and install requirements into it
    - `cd /usr/local/lib/arp-network-scanner`
    - `python3 -m venv venv3`
    - `source venv3/bin/activate`
    - `pip install --upgrade pip`
    - `pip install -r requirements.txt`

5. Start the service
    - `sudo systemctl start arp-network-scanner`

6. Enable the service at boot (so it starts when the system starts)
    - `sudo systemctl enable arp-network-scanner`

You can now see if your service is running with: `sudo systemctl status arp-network-scanner`, or see its logs with `sudo journalctl -u arp-network-scanner`.

## Usage

1. Start the service and keep it running.

2. To list the unused IPs you can use the evaluation script `python /usr/local/lib/arp-network-scanner/evaluate.py`