'''
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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

# https://github.com/FalkTannhaeuser/python-onvif-zeep
from onvif import ONVIFCamera


class CommonNetOnvif(object):
    def __init__(self, hostname="192.168.1.1", port=80, username="user",
                 password="password"):
        self.onvif_device = ONVIFCamera(hostname, port, username, password, '/etc/onvif/wsdl/')

    def com_net_onvif_get_hostname(self):
        self.onvif_device.devicemgmt.GetHostname()

    def com_net_onvif_get_time(self):
        self.onvif_device.devicemgmt.GetSystemDateAndTime()
