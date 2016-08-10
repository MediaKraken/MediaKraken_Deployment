'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

import logging
import os
import re
import time
from threading import Thread
import urllib2
import socket
import sys
from plyer import email
import psutil
import ipgetter
sys.path.append("../MediaKraken_Common/lib")
sys.path.append("../../MediaKraken_Common/lib")
import wol


# download image file from specified url to save in specific directory
def MK_Network_Fetch_From_URL(url, directory=None):
    try:
        imageFile = urllib2.urlopen(url)
        if directory is not None:
            localFile = open(directory, 'wb')
            localFile.write(imageFile.read())
            imageFile.close()
            localFile.close()
    except urllib2.URLError, e:
        logging.error('you got an error with the code %s', e)
        return None
    if directory is None:
        return imageFile.read()


# send wake on lan even to mac address
def MK_Network_WOL(mac_address):
    wol.send_magic_packet(mac_address)


# send email
def MK_Network_Send_Email(email_receipient, email_subject, email_body):
    email.send(recipient=email_receipient, subject=email_subject, text=email_body, create_chooser=True)


# get MAC address
def MK_Network_Get_MAC():
    from uuid import getnode
    return ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))


# get outside ip addy
def MK_Network_Get_Outside_IP():
    #whatismyip = 'http://checkip.dyndns.org/'
    #return urllib.urlopen(whatismyip).readlines()[0].split(':')[1].split('<')[0]
    return ipgetter.myip()


# get default ip address
def MK_Network_Get_Default_IP():
    oct_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    oct_socket.connect(('8.8.8.8', 80))
    return_data = (oct_socket.getsockname()[0])
    oct_socket.close()
    return return_data


# ping modules
class pingit(Thread):
    def __init__(self, ip):
       Thread.__init__(self)
       self.ip = ip
       self.status = -1


    def run(self):
       pingaling = None
       if str.upper(sys.platform[0:3]) == 'WIN' \
       or str.upper(sys.platform[0:3]) == 'CYG':
           pingaling = os.popen("ping -n 2 "+self.ip, "r")
       else:
           pingaling = os.popen("ping -q -c2 "+self.ip, "r")
       while 1:
           line = pingaling.readline()
           if not line: break
           igot = re.findall(pingit.lifeline, line)
           if igot:
               self.status = int(igot[0])


# ping host list
def MK_Network_Ping_List(host_list):
    pingit.lifeline = re.compile(r"(\d) received")
    report = ("No response", "Partial Response", "Alive")
    pinglist = []
    for host in host_list:
       current = pingit(host)
       pinglist.append(current)
       current.start()
    for pingle in pinglist:
       pingle.join()
       logging.info("Status from %s is %s", pingle.ip, report[pingle.status])


# get network io
def MK_Network_IO_Counter(show_nic=False):
    return psutil.net_io_counters(pernic=show_nic)


# show network connections
def MK_Network_Connections():
    return psutil.net_connections()


# show ip addys
def MK_Network_IP_Addr():
    return psutil.net_if_addrs()


# show netowrk stats
def MK_Network_Stats():
    return psutil.net_if_stats()
