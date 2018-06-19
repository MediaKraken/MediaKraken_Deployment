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


import json

from . import common_network


def com_irdb_brand_list():
    """
    # get brand list
    """
    return json.loads(common_network.mk_network_fetch_from_url('http://irdb.tk/api/brand/', None))


def com_irdb_device_types_by_brand(brand_text):
    """
    # get device types by brand
    """
    return json.loads(common_network.mk_network_fetch_from_url(
        'http://irdb.tk/api/devicetype/?brand=' + brand_text, None))


def com_irdb_codesets_brand_device(brand_text, device_type):
    """
    # See which sets of codes we have for that brand and device type:
    """
    return json.loads(common_network.mk_network_fetch_from_url(
        'http://irdb.tk/api/codeset/?brand=' + brand_text + '&devicetype=' + device_type, None))


def com_irdb_function_list(brand_text, protocol_type, device_type, device_num, subdevice):
    """
    # get the code with the protocol, device, and subdevice information we just derived from above:
    """
    return json.loads(common_network.mk_network_fetch_from_url('http://irdb.tk/api/code/?brand='
                                                               + brand_text + '&devicetype='
                                                               + device_type + '&protocol='
                                                               + protocol_type
                                                               + '&device=' + device_num
                                                               + '&subdevice=' + subdevice,
                                                               None))
