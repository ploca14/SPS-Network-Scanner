#!/bin/bash

mkdir /usr/local/lib/arp-network-scanner
cp requirements.txt evaluate.py scanner.py service.py /usr/local/lib/arp-network-scanner
cp evalarp /usr/bin
chown root:root /usr/local/lib/arp-network-scanner/service.py
chown root:root /usr/bin/evaluate
chmod 644 /usr/local/lib/arp-network-scanner/service.py
chmod +x /usr/bin/evalarp

cp -v arp-network-scanner.service /etc/systemd/system/
chown root:root /etc/systemd/system/arp-network-scanner.service
chmod 644 /etc/systemd/system/arp-network-scanner.service

cd /usr/local/lib/arp-network-scanner
python3 -m venv venv3
source venv3/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
