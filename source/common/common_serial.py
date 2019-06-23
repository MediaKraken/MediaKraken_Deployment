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

import time

from kivy.utils import platform

# import the pyserial library for use in rs232c communications
if platform != 'android':
    import serial


class CommonSerial:
    """
    Class for interfacing via serial devices
    """

    def __init__(self, dev_port='/dev/ttyUSB1', dev_baudrate=9600,
                 dev_parity=serial.PARITY_ODD,
                 dev_stopbits=serial.STOPBITS_TWO,
                 dev_bytesize=serial.SEVENBITS):
        """
        Open serial device for read/write
        """
        self.serial_device = serial.Serial(port=dev_port,
                                           baudrate=dev_baudrate,
                                           parity=dev_parity,
                                           stopbits=dev_stopbits,
                                           bytesize=dev_bytesize
                                           )
        self.serial_device.open()
        self.serial_device.isOpen()

    def com_serial_read_device(self):
        """
        Read data from serial device
        """
        time.sleep(1)
        read_data = ''
        while self.serial_device.inWaiting() > 0:
            read_data += self.serial_device.read(1)
        return read_data

    def com_serial_close_device(self):
        """
        Close serial device
        """
        self.serial_device.close()

    def com_serial_write_device(self, message):
        """
        Send data to serial device
        """
        self.serial_device.write(message)
