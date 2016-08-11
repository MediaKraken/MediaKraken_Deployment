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
import logging
from kivy.utils import platform
# import the pyserial library for use in rs232c communications
if platform != 'android':
    import serial


class MK_Common_Serial_API:
    def __init__(self):
        pass


    def MK_Serial_Open_Device(self, dev_port, dev_baudrate, dev_parity, dev_stopbits, dev_bytesize):
        self.ser_device = serial.Serial(
            #port='/dev/ttyUSB1',
            port=dev_port,
            #baudrate=9600,
            baudrate=dev_baudrate,
            #parity=serial.PARITY_ODD,
            parity=dev_parity,
            #stopbits=serial.STOPBITS_TWO,
            stopbits=dev_stopbits,
            #bytesize=serial.SEVENBITS
            bytesize=dev_bytesize
        )
        self.ser_device.open()
        self.ser_device.isOpen()


    def MK_Serial_Read_Device(self):
        time.sleep(1)
        read_data = ''
        while self.ser_device.inWaiting() > 0:
            read_data += self.ser_device.read(1)
        return read_data


    def MK_Serial_Close_Device(self):
        self.ser_device.close()


    def MK_Serial_Write_Device(self, message):
        self.ser_device.write(message)
