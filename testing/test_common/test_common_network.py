'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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


import pytest
import sys
sys.path.append("../common")
from MK_Common_Network import *


# download image file from specified url to save in specific directory
# def MK_Network_Fetch_From_URL(url, directory=None):


# send wake on lan even to mac address
# def MK_Network_WOL(mac_address):


# send email
@pytest.mark.parametrize(("email_receipient", "email_subject", "email_body"), [
    ('spootdevfake@gmail.com', "test1", "body"),
    ('spootdev@gmail.com', "test2", "body"),
    ('spootdev@fakegmail.com', "test3", "body")])
def test_MK_Network_Send_Email(email_receipient, email_subject, email_body):
    MK_Network_Send_Email(email_receipient, email_subject, email_body)


# get MAC address
def test_MK_Network_Get_MAC():
    MK_Network_Get_MAC()


# get outside ip addy
def test_MK_Network_Get_Outside_IP():
    MK_Network_Get_Outside_IP()


# get default ip address
def test_MK_Network_Get_Default_IP():
    MK_Network_Get_Default_IP()


# ping modules
#class pingit(Thread):
#    def __init__(self, ip):
#       Thread.__init__(self)
#       self.ip = ip
#       self.status = -1
#
#
#    def run(self):
#       pingaling = None
#       if str.upper(sys.platform[0:3]) == 'WIN' \
#       or str.upper(sys.platform[0:3]) == 'CYG':
#           pingaling = os.popen("ping -n 2 "+self.ip, "r")
#       else:
#           pingaling = os.popen("ping -q -c2 "+self.ip, "r")
#       while 1:
#           line = pingaling.readline()
#           if not line: break
#           igot = re.findall(pingit.lifeline, line)
#           if igot:
#               self.status = int(igot[0])


# ping host list
host_list = ('www.yahoo.com', 'www.cnn.com', '8.8.8.8')
def test_MK_Network_Ping_List():
    MK_Network_Ping_List(host_list)


# get network io
@pytest.mark.parametrize(("show_nic"), [
    (False),
    (True)])
def test_MK_Network_IO_Counter(show_nic):
    MK_Network_IO_Counter(show_nic)


# show network connections
def test_MK_Network_Connections():
    MK_Network_Connections()


# show ip addys
def test_MK_Network_IP_Addr():
    MK_Network_IP_Addr()


# show netowrk stats
def test_MK_Network_Stats():
    MK_Network_Stats()
