from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from tabulate import *

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('/usr/local/lib/arp-network-scanner/db.json', storage=serialization)

headers = {
    "ip": "IP",
    "mac": "MAC",
    "lastSeen": "Last Seen"
}

# results = sorted(db.all(),  key=lambda k: socket.inet_aton(k['ip'])) # Sort by ip
results = sorted(db.all(),  key=lambda k: k['lastSeen'])

print(tabulate(results, headers=headers))