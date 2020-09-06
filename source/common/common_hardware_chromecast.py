"""
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
"""

import requests
import xmltodict

from . import common_global
from . import common_network_ssdp

CAST_PLAYER_APPID = "CC1AD845"


# hardware stats for supported images/etc
# https://developers.google.com/cast/docs/media

def com_hard_chrome_discover(timeout=5, retries=1):
    """
    Discover chromecast devices
    """
    device_list = common_network_ssdp.ssdp_discover(
        service='urn:dial-multiscreen-org:device:dial:1',
        timeout=timeout,
        retries=retries, mx=1)
    devices_found = []
    for ssdp_device_location in device_list:
        # get the info via request and xmltodict
        chrome_info = com_hard_chrome_info(ssdp_device_location)
        # verify that it is indeed a chromecast
        if chrome_info['root']['device']['deviceType'] == 'urn:dial-multiscreen-org:device:dial:1':
            print(ssdp_device_location, flush=True)
            # print(type(chrome_info), flush=True)
            # print(chrome_info['root'], flush=True)
            # print(chrome_info['root']['device'], flush=True)
            # print(chrome_info['root']['device']['deviceType'], flush=True)
            # print(chrome_info['root']['device']['modelName'], flush=True)
            # print(chrome_info['root']['device']['friendlyName'], flush=True)
            devices_found.append((ssdp_device_location.rsplit(':', 1)[0].split('//', 1)[1],
                                  chrome_info['root']['device']['modelName'],
                                  chrome_info['root']['device']['friendlyName']))
    return devices_found


def com_hard_chrome_info(ssdp_device_location):
    """
    get info of chromecast
    """
    chrome_data = requests.get(ssdp_device_location, timeout=5)
    return xmltodict.parse(chrome_data.text)


def com_hard_chrome_play_youtube(youtube_video_guid, ip_addr, port=8008):
    response = requests.post(('http://%s:%s/apps/YouTube' % (ip_addr, port)),
                             data={'v': youtube_video_guid})
    if response.status_code != 200:
        if common_global.es_inst is not None:
            common_global.es_inst.com_elastic_index('info', {'yt play guid': youtube_video_guid})


def com_hard_chrome_youtube_stop(ip_addr, port=8008):
    response = requests.delete('http://%s:%s/apps/YouTube' % (ip_addr, port))
    if response.status_code != 200:
        if common_global.es_inst is not None:
            common_global.es_inst.com_elastic_index('info', {'yt stop ip_addr': ip_addr})

# TODO http://CHROMECAST_IP:8008/ssdp/device-desc.xml
# TODO http://CHROMECAST_IP:8008/apps/ChromeCast
# TODO http://CHROMECAST_IP:8008/apps/
