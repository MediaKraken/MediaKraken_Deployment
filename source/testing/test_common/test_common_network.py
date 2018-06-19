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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_network


# download image file from specified url to save in specific directory
# def mk_network_fetch_from_url(url, directory=None):


# send wake on lan even to mac address
# def mk_network_wol(mac_address):


# get MAC address
def test_mk_network_get_mac():
    """
    Test function
    """
    common_network.mk_network_get_mac()


# get outside ip addy
def test_mk_network_get_outside_ip():
    """
    Test function
    """
    common_network.mk_network_get_outside_ip()


# get default ip address
def test_mk_network_get_default_ip():
    """
    Test function
    """
    common_network.mk_network_get_default_ip()


# ping modules
# class pingit(Thread):
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


host_list = ('www.yahoo.com', 'www.cnn.com', '8.8.8.8')


def test_mk_network_ping_list():
    """
    # ping host list
    """
    common_network.mk_network_ping_list(host_list)


@pytest.mark.parametrize(("show_nic"), [
    (False),
    (True)])
def test_mk_network_io_counter(show_nic):
    """
    # get network io
    """
    common_network.mk_network_io_counter(show_nic)


def test_mk_network_connections():
    """
    # show network connections
    """
    common_network.mk_network_connections()


def test_mk_network_ip_addr():
    """
    # show ip addys
    """
    common_network.mk_network_ip_addr()


def test_mk_network_stats():
    """
    # show network stats
    """
    common_network.mk_network_stats()
