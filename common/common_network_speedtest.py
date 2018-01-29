'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import logging  # pylint: disable=W0611
import pyspeedtest


class CommonNetworkSpeedtest(object):
    """
    Class for interfacing with speedtest
    """

    def __init__(self, access_token):
        self.st = pyspeedtest.SpeedTest()

    def com_net_st_ping(self):
        return self.st.ping()

    def com_net_st_dl(self):
        return self.st.download()

    def com_net_st_ul(self):
        return self.st.upload()
