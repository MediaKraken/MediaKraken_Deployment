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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import nest
from nest import utils as nest_utils


def com_nest_device_connect(user_name, password):
    """
    Connect to NEST
    """
    nest_device = nest.Nest(user_name, password)
    return nest_device


def com_nest_device_structures(nest_device):
    """
    # grab structures and the devices
    """
    for structure in nest_device.structures:
        logging.info('Structure %s', structure.name)
        logging.info('Away: %s', structure.away)
        logging.info('Devices:')
        for device in structure.devices:
            logging.info('Device: %s', device.name)
            logging.info('Temp: %0.1f', device.temperature)


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
