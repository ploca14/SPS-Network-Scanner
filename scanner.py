import logging
import os
from scapy.all import *
from scapy.all import ARP
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

logger = logging.getLogger(f"main.{__name__}")
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

file_path = os.path.dirname(__file__)
db = TinyDB(file_path + '/db.json', storage=serialization)

def main():
    logger.info("Started sniffing")
    sniff(prn=arp_monitor_callback, filter="arp", store=0)

def arp_monitor_callback(pkt):
    if ARP in pkt:
        ip = pkt.sprintf("%ARP.psrc%")
        mac = pkt.sprintf("%ARP.hwsrc%")
        iface = pkt.sniffed_on.description

        Record = Query()
        db.upsert({
            'iface': iface,
            'ip': ip,
            'mac': mac,
            'lastSeen': datetime.now(),
        }, Record.ip == ip)
        logger.info(pkt.sprintf(" Sniffed arp packet from: %ARP.hwsrc% %ARP.psrc%"))
