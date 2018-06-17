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
from common import common_network_irdb


# get brand list
def test_com_irdb_brand_list():
    common_network_irdb.com_irdb_brand_list()


# get device types by brand
@pytest.mark.parametrize(("brand_text"), [
    ("Pioneer"),
    ("Sony"),
    ("FakeBrand")])
def test_com_irdb_device_types_by_brand(brand_text):
    """
    Test function
    """
    common_network_irdb.com_irdb_device_types_by_brand(brand_text)

# See which sets of codes we have for that brand and device type:
# def com_IRDB_Codesets_by_Brand_Device(brand_text, device_type):


# get the code with the protocol, device, and subdevice information we just derived from above:
# def com_IRDB_Function_List(brand_text, protocol_type, device_type, device_num, subdevice):
