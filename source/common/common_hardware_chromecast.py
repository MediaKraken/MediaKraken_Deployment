'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

from __future__ import absolute_import, division, print_function, unicode_literals

import httplib
import socket

import xmltodict

from . import common_global

CAST_PLAYER_APPID = "CC1AD845"


# hardware stats for supported images/etc
# https://developers.google.com/cast/docs/media

def com_hard_chrome_discover(timeout=5, retries=1):
    """
    Discover chromecast devices
    """
    message = "\r\n".join(['M-SEARCH * HTTP/1.1',
                           'HOST: 239.255.255.250:1900',
                           'MAN: "ssdp:discover"',
                           'MX: 1',
                           'ST: urn:dial-multiscreen-org:service:dial:1',
                           '', ''])
    socket.setdefaulttimeout(timeout)
    # do the actual ssdp calls
    devices_found = {}
    for _ in range(retries):
        ssdp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ssdp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssdp_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        ssdp_sock.sendto(message, ("239.255.255.250", 1900))
        while True:
            try:
                response = ssdp_sock.recv(1024)
                common_global.es_inst.com_elastic_index('info', {'response body': response})
            except socket.timeout:
                common_global.es_inst.com_elastic_index('error', {'socket timeout'})
                break
        ssdp_sock.close()
    return devices_found


def com_hard_chrome_name(ip_addr):
    """
    get name of chromecast
    """
    http_conn = httplib.HTTPConnection(ip_addr + ":8008")
    http_conn.request("GET", "/ssdp/device-desc.xml")
    http_resp = http_conn.getresponse()
    if http_resp.status == 200:
        status_doc = http_resp.read()
        common_global.es_inst.com_elastic_index('info', {'name data': status_doc})
        return xmltodict.parse(status_doc)
    else:
        return None
