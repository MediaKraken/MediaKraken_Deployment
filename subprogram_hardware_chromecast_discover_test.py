'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import logging # pylint: disable=W0611
from common import common_hardware_chromecast
import json

# look for devices
chrome = common_hardware_chromecast.CommonHardwareChromecast()
#print("Chrome: ", chrome)
#print(chrome.count)
#print(chrome.devices)
for row_data in chrome.com_chromecast_discover():
    print("Chromecast: ", row_data)
    print("device: ", row_data.device)
    print("port: ", row_data.port)
    #print("Dev: ", row_data.device)
    print("Friendly Name: ", row_data.device.friendly_name)
    print("Model Name: ", row_data.device.model_name)
    print("Manufacture: ", row_data.device.manufacturer)
    print("API: ", row_data.device.api_version)
    print("UUID: ", row_data.device.uuid)
    print("Type: ", row_data.device.cast_type)

    print("Stat: ", row_data.status)
    #cast_json = chrome.com_chromecast_info()
    #print("Cast: %s", cast_json)
    # print("status: %s" % chrome.com_chromecast_status())
