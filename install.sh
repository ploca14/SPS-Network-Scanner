#!/bin/bash

mkdir /usr/local/lib/arp-network-scanner
cp requirements.txt evaluate.py scanner.py service.py /usr/local/lib/arp-network-scanner
chown root:root /usr/local/lib/arp-network-scanner/service.py
chmod 644 /usr/local/lib/arp-network-scanner/service.py

cp -v arp-network-scanner.service /etc/systemd/system/
chown root:root /etc/systemd/system/arp-network-scanner.service
chmod 644 /etc/systemd/system/arp-network-scanner.service

cd /usr/local/lib/arp-network-scanner
python3 -m venv venv3
source venv3/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
