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

from __future__ import absolute_import, division, print_function, unicode_literals
import pytest  # pylint: disable=W0611
import sys

sys.path.append('.')
from common import common_serial


class TestCommonSerial(object):

    @classmethod
    def setup_class(self):
        self.serial_connection = common_serial.CommonSerial()

    @classmethod
    def teardown_class(self):
        pass

    #    def MK_Serial_Open_Device(self, dev_port, dev_baudrate, dev_parity, dev_stopbits, dev_bytesize):

    def test_com_serial_read_device(self):
        """
        Test function
        """
        self.serial_connection.com_serial_read_device()

    def test_com_serial_close_device(self):
        """
        Test function
        """
        self.serial_connection.com_serial_close_device()

    def test_com_serial_write_device(self):
        """
        Test function
        """
        self.serial_connection.com_serial_write_device("Test serial message")
