import logging
import sched
from scapy.all import *
from scapy.layers.l2 import arping
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from interfaces import getInetfacesNetworks

logger = logging.getLogger(f"main.{__name__}")
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

file_path = os.path.dirname(__file__)
db = TinyDB(file_path + '/arp-network-scanner-db.json', storage=serialization)
Record = Query()

ifnetworks = getInetfacesNetworks()

s = sched.scheduler(time.time, time.sleep)

def main():
    logger.info("Started arp scanner")
    logger.info("Found following ethernet ifaces: " + str(ifnetworks.keys()))
    try:
        s.enter(1, 1, arpscan, (s,))
        s.run()
    except Exception as e:
        logger.info("Stopping arp scanner")
        exit(0)

def arpscan(sc):
    for iface, networks in ifnetworks.items():
        for network in networks:
            ping = arping(network.with_prefixlen)

            for pkt in ping[0]:
                ip = pkt.answer.sprintf("%ARP.psrc%")
                mac = pkt.answer.sprintf("%ARP.hwsrc%")

                db.upsert({
                    'iface': iface,
                    'ip': ip,
                    'mac': mac,
                    'lastSeen': datetime.now(),
                }, Record.ip == ip)
            logger.info("Finished arping on iface: " + iface)

    sc.enter(15*60, 1, arpscan, (sc,))
