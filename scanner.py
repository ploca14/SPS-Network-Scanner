#! /usr/bin/env python
from scapy.all import *
import logging

logging.basicConfig(level=logging.DEBUG)

cache = []
def updateCache(pkt):
    cache.append(pkt)

def arp_monitor_callback(pkt): #who-has or is-at
    updateCache(pkt)
    logging.info(pkt.sprintf(" Sniffed arp packet from: %ARP.hwsrc% %ARP.psrc%"))


sniff(prn=arp_monitor_callback, filter="arp", store=0)
#wrpcap na ulozeni historie na disk (pokud bude program resetovany)