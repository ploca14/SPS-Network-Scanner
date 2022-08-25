from datetime import datetime, timedelta
import subprocess
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from tabulate import tabulate
import scapy.interfaces
from scapy.all import *
import ipaddress
import sys

args = sys.argv

if not len(args) in range(2, 4):
    raise AttributeError("Invalid arguments: " + str(args))

unit = args[1]
length = 1

if len(args) == 3:
    length = args[2]
    length = int(length)

if length <= 0 or length > 1000:
    raise AttributeError("Length must be an integer between 1-1000.")

dateLimit = 0
listAll = False
listNotSeen = False

if unit == 'd':
    dateLimit = datetime.now() - timedelta(days=length)
elif unit == 'w':
    dateLimit = datetime.now() - timedelta(weeks=length)
elif unit == 'm':
    dateLimit = datetime.now() - timedelta(weeks=length*30)
elif unit == 'h':
    dateLimit = datetime.now() - timedelta(hours=length)
elif unit == 'a':
    listAll = True
elif unit == 'n':
    listNotSeen = True
else:
    raise AttributeError("Invalid unit of time. Days, weeks and months are supported.")

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('/usr/local/lib/arp-network-scanner/arp-network-scanner-db.json', storage=serialization)

headers = {
    "ip": "IP",
    "mac": "MAC",
    "lastSeen": "Last Seen",
    "iface": "Interface"
}

# results = sorted(db.all(),  key=lambda k: socket.inet_aton(k['ip'])) # Sort by ip
results = sorted(db.all(), key=lambda k: k['iface'])

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


def getNotSeen():
    empty_results = []
    for iface, network in networks.items():
        for ip in network.hosts():
            empty_result = {
                'iface': iface,
                'ip': str(ip),
                'mac': None,
                'lastSeen': 'Never'
            }
            containsResult = list(filter(lambda result: result.get('ip') == empty_result.get('ip'), results))
            if len(containsResult) == 0:
                empty_results.append(empty_result)
    return empty_results

if listAll:
    print(tabulate(results, headers=headers))
    exit(0)

if listNotSeen:
    print(tabulate(getNotSeen(), headers=headers))
    exit(0)

filteredResults = filter(lambda result: result.get('lastSeen') <= dateLimit, results)

print(tabulate(filteredResults, headers=headers))

