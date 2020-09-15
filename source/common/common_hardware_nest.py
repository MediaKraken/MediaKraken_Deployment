"""
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
"""

import nest
from common import common_logging_elasticsearch_httpx
from nest import utils as nest_utils


class CommonHardwareNest:
    """
    Class for interfacing with arduino device over usb
    """

    def __init__(self, user_name, password):
        """
        Connect to NEST
        """
        self.nest_device = nest.Nest(user_name, password)

    def com_nest_device_structures(self):
        """
        # grab structures and the devices
        """
        for structure in self.nest_device.structures:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={'Structure':
                                                                                   structure.name,
                                                                               'Away':
                                                                                   structure.away})
            for device in structure.devices:
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'Device': device.name})
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'Temp': device.temperature})


def com_nest_c_to_f(temp_data):
    """
    C to F temp conversion
    """
    return nest_utils.c_to_f(temp_data)


def com_nest_f_to_c(temp_data):
    """
    F to C temp conversion
    """
    return nest_utils.f_to_c(temp_data)
