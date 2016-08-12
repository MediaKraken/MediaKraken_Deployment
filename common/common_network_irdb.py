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

# interface for IRDB website

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import json
import sys
# include code from other paths
sys.path.append("../../MediaKraken_Common/")
import common_network


# get brand list
def com_IRDB_Brand_List():
    return json.loads(com_network.MK_Network_Fetch_From_URL('http://irdb.tk/api/brand/', None))


# get device types by brand
def com_IRDB_Device_Types_By_Brand(brand_text):
    return json.loads(com_network.MK_Network_Fetch_From_URL('http://irdb.tk/api/devicetype/?brand=' + brand_text, None))


# See which sets of codes we have for that brand and device type:
def com_IRDB_Codesets_By_Brand_Device(brand_text, device_type):
    return json.loads(com_network.MK_Network_Fetch_From_URL('http://irdb.tk/api/codeset/?brand='\
        + brand_text + '&devicetype=' + device_type, None))


# get the code with the protocol, device, and subdevice information we just derived from above:
def com_IRDB_Function_List(brand_text, protocol_type, device_type, device_num, subdevice):
    return json.loads(com_network.MK_Network_Fetch_From_URL('http://irdb.tk/api/code/?brand='\
        + brand_text + '&devicetype=' + device_type + '&protocol=' + protocol_type\
        + '&device=' + device_num + '&subdevice=' + subdevice, None))
