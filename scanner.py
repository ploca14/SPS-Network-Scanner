import logging
import sched
import ipaddress
from scapy.all import *
from scapy.layers.l2 import arping
import scapy.interfaces
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

logger = logging.getLogger(f"main.{__name__}")
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

file_path = os.path.dirname(__file__)
db = TinyDB(file_path + '/arp-network-scanner-db.json', storage=serialization)

networks = {}
for iface in scapy.interfaces.get_working_ifaces():
    if 'eth' in iface.name or 'enp' in iface.name:
        nmcmd = "ifconfig %s | grep netmask | awk {'print $4'}" % (iface.name)
        netmask = subprocess.Popen(nmcmd, shell=True, stdout=subprocess.PIPE)
        netmask = netmask.stdout.read()
        netmask = str(netmask).strip('b').strip('\'').strip('\\n')
        ip = iface.ip
        if ip is not None:
            networks[iface.name] = ipaddress.IPv4Network(iface.ip + '/' + netmask, False)


s = sched.scheduler(time.time, time.sleep)

def main():
    logger.info("Started arp scanner")
    logger.info("Found following ethernet ifaces: " + str(networks.keys()))
    try:
        s.enter(1, 1, arpscan, (s,))
        s.run()
    except Exception as e:
        logger.info("Stopping arp scanner")
        exit(0)

def arpscan(sc):
    for iface, network in networks.items():
        ping = arping(network.with_prefixlen)

        for pkt in ping[0]:
            ip = pkt.answer.sprintf("%ARP.psrc%")
            mac = pkt.answer.sprintf("%ARP.hwsrc%")

            Record = Query()
            db.upsert({
                'iface': iface,
                'ip': ip,
                'mac': mac,
                'lastSeen': datetime.now(),
            }, Record.ip == ip)
        logger.info("Finished arping on iface: " + iface)

    sc.enter(15*60, 1, arpscan, (sc,))
