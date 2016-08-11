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
sys.path.append("../common/lib")
sys.path.append("../../common/lib")
import wol


def MK_Network_Fetch_From_URL(url, directory=None):
    """
    Download image file from specified url to save in specific directory
    """
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


def MK_Network_WOL(mac_address):
    """
    Send wake on lan even to mac address
    """
    wol.send_magic_packet(mac_address)


def MK_Network_Send_Email(email_receipient, email_subject, email_body):
    """
    Send email
    """
    email.send(recipient=email_receipient, subject=email_subject, text=email_body, create_chooser=True)


def MK_Network_Get_MAC():
    """
    Get MAC address
    """
    from uuid import getnode
    return ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))


def MK_Network_Get_Outside_IP():
    """
    Get outside ip addy
    """
    #whatismyip = 'http://checkip.dyndns.org/'
    #return urllib.urlopen(whatismyip).readlines()[0].split(':')[1].split('<')[0]
    return ipgetter.myip()


def MK_Network_Get_Default_IP():
    """
    Get default ip address
    """
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


def MK_Network_Ping_List(host_list):
    """
    Ping host list
    """
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


def MK_Network_IO_Counter(show_nic=False):
    """
    Get network io
    """
    return psutil.net_io_counters(pernic=show_nic)


def MK_Network_Connections():
    """
    Show network connections
    """
    return psutil.net_connections()


def MK_Network_IP_Addr():
    """
    Show ip addys
    """
    return psutil.net_if_addrs()


def MK_Network_Stats():
    """
    Show netowrk stats
    """
    return psutil.net_if_stats()
