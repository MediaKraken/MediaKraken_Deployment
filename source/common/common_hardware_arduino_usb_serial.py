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

from Arduino import Arduino


class CommonHardwareArduino:
    """
    Class for interfacing with arduino device over usb
    """

    def __init__(self, baud_rate='9600', device_port="/dev/ttyACM0"):
        self.arduino_device = Arduino(baud_rate, port=device_port)

    # 'LOW'
    def com_arduino_usb_serial_digitalwrite(self, pin_number, pin_high_low='HIGH'):
        self.arduino_device.digitalWrite(pin_number, pin_high_low)

    def com_arduino_usb_serial_writestring(self, serial_string):
        self.arduino_device.SoftwareSerial.write(serial_string)

    def com_arduino_usb_serial_receivestring(self):
        pass
