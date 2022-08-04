import datetime
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from tabulate import *
import sys

args = sys.argv

if len(args) != 3 and len(args) != 1:
    raise AttributeError("Option and value are required as arguments.")

unit = args[1]
length = args[2]
length = int(length)

if length <= 0 or length > 1000:
    raise AttributeError("Length must be an integer between 1-1000.")

dateLimit = 0

if unit == 'd':
    dateLimit = datetime.datetime.now() - datetime.timedelta(days=length)
elif unit == 'w':
    dateLimit = datetime.datetime.now() - datetime.timedelta(weeks=length)
elif unit == 'm':
    dateLimit = datetime.datetime.now() - datetime.timedelta(weeks=length*30)
else:
    raise AttributeError("Invalid unit of time. Days, weeks and months are supported.")

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

filteredResults = []

for result in results:
    if result.get('lastSeen') <= dateLimit:
        filteredResults.append(result)

filteredResults = sorted(filteredResults,  key=lambda k: k['lastSeen'])

print(tabulate(filteredResults, headers=headers))
