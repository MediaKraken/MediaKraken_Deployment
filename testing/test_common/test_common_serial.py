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
import pytest
import sys
sys.path.append("../common")
from MK_Common_Serial import *


class Test_MK_Common_Serial_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Serial_API()


    @classmethod
    def teardown_class(self):
        pass


#    def MK_Serial_Open_Device(self, dev_port, dev_baudrate, dev_parity, dev_stopbits, dev_bytesize):


    def test_MK_Serial_Read_Device(self):
        self.db.MK_Serial_Read_Device()


    def test_MK_Serial_Close_Device(self):
        self.db.MK_Serial_Close_Device()


    def test_MK_Serial_Write_Device(self):
        self.db.MK_Serial_Write_Device("Test serial message")
