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

import http.client
import socket

import requests
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
                if common_global.es_inst != None:
                    common_global.es_inst.com_elastic_index('info', {'response body': response})
                for line in response.split("\r\n"):
                    if line.find('LOCATION') == 0:
                        # pull out the ip
                        device_location = line.split(':', 1)[1].strip()[7:].split(':', 1)[0]
                    elif line.find('ST') == 0 and line.find(
                            'urn:dial-multiscreen-org:service:dial:1') != -1:
                        # this is a chromecast device so grab the model and name
                        chrome_info = com_hard_chrome_info(device_location)
                        devices_found[device_location] = (
                            chrome_info['root']['device']['modelName'],
                            chrome_info['root']['device']['friendlyName'])
            except socket.timeout:
                if common_global.es_inst != None:
                    common_global.es_inst.com_elastic_index('error', {'socket timeout'})
                break
        ssdp_sock.close()
    return devices_found


def com_hard_chrome_info(ip_addr):
    """
    get info of chromecast
    """
    http_conn = http.client.HTTPConnection(ip_addr + ":8008")
    http_conn.request("GET", "/ssdp/device-desc.xml")
    http_resp = http_conn.getresponse()
    if http_resp.status == 200:
        status_doc = http_resp.read()
        if common_global.es_inst != None:
            common_global.es_inst.com_elastic_index('info', {'name data': status_doc})
        return xmltodict.parse(status_doc)
    else:
        return None


def com_hard_chrome_play_youtube(youtube_video_guid, ip_addr, port=8008):
    response = requests.post(('http://%s:%s/apps/YouTube' % (ip_addr, port)),
                             data={'v': youtube_video_guid})
    if response.status_code != 200:
        if common_global.es_inst != None:
            common_global.es_inst.com_elastic_index('info', {'yt play guid': youtube_video_guid})


def com_hard_chrome_youtube_stop(ip_addr, port=8008):
    response = requests.delete('http://%s:%s/apps/YouTube' % (ip_addr, port))
    if response.status_code != 200:
        if common_global.es_inst != None:
            common_global.es_inst.com_elastic_index('info', {'yt stop ip_addr': ip_addr})

# TODO http://CHROMECAST_IP:8008/ssdp/device-desc.xml
# TODO http://CHROMECAST_IP:8008/apps/ChromeCast
# TODO http://CHROMECAST_IP:8008/apps/
