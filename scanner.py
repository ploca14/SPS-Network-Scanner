#! /usr/bin/env python
from scapy.all import *
import logging

logging.basicConfig(level=logging.DEBUG)

cache = []

def arp_monitor_callback(pkt):
    cache.append(pkt)
    logging.info(pkt.sprintf(" Sniffed arp packet from: %ARP.hwsrc% %ARP.psrc%"))

def onShutdown():
    wrpcap("packetlog" + datetime.now().strftime('%Y-%m-%d') + ".pcap", cache)

atexit.register(onShutdown)

sniff(prn=arp_monitor_callback, filter="arp", store=0)
#wrpcap na ulozeni historie na disk (pokud bude program resetovany)