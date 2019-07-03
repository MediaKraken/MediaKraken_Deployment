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

import json
import os
import re
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from threading import Thread
from uuid import getnode

from . import common_file
from . import common_global
from . import wol


def mk_network_fetch_from_url(url, directory=None):
    """
    Download data from specified url to save in specific directory
    """
    common_global.es_inst.com_elastic_index('info', {'dl': url, 'dir': directory})
    try:
        datafile = urllib.request.urlopen(url, context=ssl._create_unverified_context())
        if directory is not None:
            try:
                localfile = open(directory, 'wb')
            except:
                # create missing directory structure
                common_file.com_mkdir_p(directory)
                localfile = open(directory, 'wb')
            try:
                localfile.write(datafile.read())
            except urllib.error.HTTPError:
                time.sleep(30)
                mk_network_fetch_from_url(url, directory)
            datafile.close()
            localfile.close()
    except urllib.error.URLError:
        common_global.es_inst.com_elastic_index('error', {'mk_network_fetch_from_url'})
        return None
    if directory is None:
        return datafile.read()
    return True


def mk_network_wol(mac_address):
    """
    Send wake on lan event to mac address
    """
    wol.send_magic_packet(mac_address)


def mk_network_get_mac():
    """
    Get MAC address
    """
    return ':'.join(("%012X" % getnode())[i:i + 2] for i in range(0, 12, 2))


def mk_network_get_outside_ip():
    """
    Get outside ip addy
    """
    url_data = str(urllib.request.urlopen('http://checkip.dyndns.org/').read())
    return url_data.split(':')[1].split('<')[0].strip()


def mk_network_get_default_ip():
    """
    Get default ip address
    """
    oct_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    oct_socket.connect(('8.8.8.8', 80))
    return_data = (oct_socket.getsockname()[0])
    oct_socket.close()
    return return_data


class PingIt(Thread):
    """
    # ping modules
    """

    def __init__(self, ip_addr):
        Thread.__init__(self)
        self.ip_addr = ip_addr
        self.status = -1

    def run(self):
        """
        run the pings
        """
        pingaling = None
        # if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        #     pingaling = os.popen("ping -n 2 " + self.ip_addr, "r")
        # else:
        pingaling = os.popen("ping -q -c2 " + self.ip_addr, "r")
        while 1:
            line = pingaling.readline()
            if not line:
                break
            igot = re.findall(PingIt.lifeline, line)
            if igot:
                self.status = int(igot[0])


def mk_network_ping_list(host_list):
    """
    Ping host list
    """
    PingIt.lifeline = re.compile(r"(\d) received")
    report = ("No response", "Partial Response", "Alive")
    pinglist = []
    for host in host_list:
        current = PingIt(host)
        pinglist.append(current)
        current.start()
    for pingle in pinglist:
        pingle.join()
        common_global.es_inst.com_elastic_index('info', {"Status from":
                                                             pingle.ip_addr,
                                                         'report': report[pingle.status]})


def mk_network_io_counter(show_nic=False):
    """
    Get network io
    """
    import psutil
    return psutil.net_io_counters(pernic=show_nic)


def mk_network_connections():
    """
    Show network connections
    """
    import psutil
    return psutil.net_connections()


def mk_network_ip_addr():
    """
    Show ip addys
    """
    import psutil
    return psutil.net_if_addrs()


def mk_network_stats():
    """
    Show network stats
    """
    import psutil
    return psutil.net_if_stats()


def mk_network_country_code():
    try:
        response = urllib.request.urlopen("https://geoip-db.com/json")
        return json.loads(response.read())
    except:
        return {'country_code': 'Error', 'country_name': 'Unknown'}


def mk_network_service_available(host_dns, host_ip, wait_seconds='30'):
    wait_pid = subprocess.Popen(
        ['/mediakraken/wait-for-it-ash.sh', '-h', host_dns, '-p', host_ip, '-t', wait_seconds],
        stdout=subprocess.PIPE, shell=False)
    wait_pid.wait()
