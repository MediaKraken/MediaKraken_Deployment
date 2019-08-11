"""
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
"""

from sense_hat import SenseHat


class CommonHardwarePISenseHat:
    """
    Class for interfacing with raspberry pi sensehat
    """

    def __init__(self):
        self.sense_inst = SenseHat()
        self.sense_inst.clear()

    def com_hard_pi_get_temp(self):
        return self.sense_inst.get_temperature()

    def com_hard_pi_get_pressure(self):
        return self.sense_inst.get_pressure()

    def com_hard_pi_get_humidity(self):
        return self.sense_inst.get_humidity()
