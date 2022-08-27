from os import listdir
from os.path import islink, realpath, join, dirname
import netifaces
from collections import defaultdict
import ipaddress

file_path = dirname(__file__)

def getInterfaces():
    interfaces = []
    with open(file_path + '/config', encoding = 'utf-8') as f:
        interfaces = f.readlines()
    
    if not interfaces:
        for i in listdir("/sys/class/net"):
            if islink(join("/sys/class/net", i)):
                if not realpath(join("/sys/class/net", i)).startswith(("/sys/devices/virtual", "/sys/devices/vif")):
                    interfaces.append(i)
    return interfaces

def getInetfacesNetworks():
    ifaddresses = defaultdict(set)
    ifaces = getInterfaces()

    for iface in ifaces:
        iface = iface.strip('\n')
        print(iface)
        try:
            addrs = netifaces.ifaddresses(iface)
        except ValueError as err:
            print(str(err))
            exit(1)
        addrs = addrs[netifaces.AF_INET]
        for addr in addrs:
            network = ipaddress.IPv4Network(addr['addr'] + '/' + addr['netmask'], False)
            ifaddresses[iface].add(network)
    return ifaddresses