from datetime import datetime, timedelta
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from tabulate import tabulate
from scapy.all import *
import sys
from interfaces import getInetfacesNetworks

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

dateLimit = datetime.min
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
    raise AttributeError("Invalid unit of time. Days, weeks, months and hours are supported.")

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('/usr/local/lib/arp-network-scanner/arp-network-scanner-db.json', storage=serialization)
Record = Query()

ifnetworks = getInetfacesNetworks()

def getNotSeen():
    empty_results = []
    for iface, networks in ifnetworks.items():
        for network in networks:
            for ip in filter(lambda x: not db.contains(Record.ip == str(x)), network.hosts()):
                empty_result = {
                    'iface': iface,
                    'ip': str(ip),
                    'mac': None,
                    'lastSeen': 'Never'
                }
                empty_results.append(empty_result)
    return empty_results

results = []
if listAll:
    results = db.all() + getNotSeen()
elif listNotSeen:
    results = getNotSeen()
else:
    results = db.search(Record.lastSeen <= dateLimit)

sortedResults = sorted(results, key=lambda k: (k['iface'], socket.inet_aton(k['ip'])))

headers = {
    "ip": "IP",
    "mac": "MAC",
    "lastSeen": "Last Seen",
    "iface": "Interface"
}

print(tabulate(sortedResults, headers=headers))