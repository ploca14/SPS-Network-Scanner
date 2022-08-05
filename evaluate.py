import datetime
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from tabulate import *
import sys

args = sys.argv

if not len(args) in range(1, 4):
    raise AttributeError("Invalid arguments.")

unit = args[1]
length = 1

if len(args) == 3:
    length = args[2]
    length = int(length)

if length <= 0 or length > 1000:
    raise AttributeError("Length must be an integer between 1-1000.")

dateLimit = 0
listAll = False

if unit == 'd':
    dateLimit = datetime.datetime.now() - datetime.timedelta(days=length)
elif unit == 'w':
    dateLimit = datetime.datetime.now() - datetime.timedelta(weeks=length)
elif unit == 'm':
    dateLimit = datetime.datetime.now() - datetime.timedelta(weeks=length*30)
elif unit == 'a':
    listAll = True
else:
    raise AttributeError("Invalid unit of time. Days, weeks and months are supported.")

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
db = TinyDB('db.json', storage=serialization)

headers = {
    "ip": "IP",
    "mac": "MAC",
    "lastSeen": "Last Seen",
    "iface": "Interface"
}

# results = sorted(db.all(),  key=lambda k: socket.inet_aton(k['ip'])) # Sort by ip
results = sorted(db.all(),  key=lambda k: k['lastSeen'])

if listAll:
    print(tabulate(results, headers=headers))
    exit(0)

filteredResults = []

for result in results:
    if result.get('lastSeen') <= dateLimit:
        filteredResults.append(result)

print(tabulate(filteredResults, headers=headers))
