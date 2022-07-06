#! /usr/bin/sudo python
from scapy.all import *
import logging

logging.basicConfig(level=logging.DEBUG)

cache = []
inMemoryAddrDB = {}

def arp_monitor_callback(pkt):
    cache.append(pkt)
    inMemoryAddrDB[ARP.hwsrc] = datetime.now()
    logging.info(pkt.sprintf(" Sniffed arp packet from: %ARP.hwsrc% %ARP.psrc%"))

def onShutdown():
    if len(cache) > 0:
        wrpcap("packetlog" + datetime.now().strftime('%Y-%m-%d') + ".pcap", cache)

atexit.register(onShutdown)

sniff(prn=arp_monitor_callback, filter="arp", store=0)

