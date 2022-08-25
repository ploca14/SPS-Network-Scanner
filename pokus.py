import subprocess

from scapy.all import *
from scapy.layers.l2 import arping
import scapy.interfaces
import ipaddress
import sched


# tuple = arping('192.168.68.0/24')

# print('Found ' + str(len(tuple[0])) + ' addresses.')

def findSubnets():
    networks = {}
    for iface in scapy.interfaces.get_working_ifaces():

        if 'eth' in iface.name or 'enp' in iface.name:
            nmcmd = "ifconfig %s | grep netmask | awk {'print $4'}" % (iface.name)
            netmask = subprocess.Popen(nmcmd, shell=True, stdout=subprocess.PIPE)
            netmask = netmask.stdout.read()
            netmask = str(netmask).strip('b').strip('\'').strip('\\n')
            # networks.append(ipaddress.IPv4Network('192.168.68.63' + '/' + '255.255.255.0', False))
    networks[iface.name] = ipaddress.IPv4Network('192.168.68.63' + '/' + '255.255.255.0', False)
    for iface, network in networks.items():
        ping = arping(network.with_prefixlen)
        for query in ping[0]:
            print(query.answer.sprintf("%ARP.psrc%"))

findSubnets()

# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc):
#     print("Doing stuff...")
#     for iface in scapy.interfaces.get_working_ifaces():
#         print(iface.ip)
#     sc.enter(2, 1, do_something, (sc,))
#
# try:
#     s.enter(2, 1, do_something, (s,))
#     s.run()
# except:
#     print("exiting")
#     exit(0)
