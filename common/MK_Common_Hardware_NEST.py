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

import logging
import nest
from nest import utils as nest_utils


# connect to NEST device
def MK_NEST_Device_Connect(user_name, password):
    nest_device = nest.Nest(user_name, password)
    return nest_device


# grab structures and the devices
def MK_NEST_Device_Structures(nest_device):
    for structure in nest_device.structures:
        logging.info('Structure %s' % structure.name)
        logging.info('Away: %s' % structure.away)
        logging.info('Devices:')
        for device in structure.devices:
            logging.info('Device: %s' % device.name)
            logging.info('Temp: %0.1f' % device.temperature)


# temp conversion
def MK_NEST_C_to_F(temp_data):
    return nest_utils.c_to_f(temp_data)


def MK_NEST_F_to_C(temp_data):
    return nest_utils.f_to_c(temp_data)
