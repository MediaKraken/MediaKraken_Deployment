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

import sys

sys.path.append('.')
from common import common_network_ssdp


class TestSSDPResponse:

    @classmethod
    def setup_class(self):
        self.ssdp_connection = common_network_ssdp.SSDPResponse()

    @classmethod
    def teardown_class(self):
        pass

# class SSDPResponse:
#    class _FakeSocket(StringIO.StringIO):
#        def makefile(self, *args, **kw):
#            return self


#    def __init__(self, response):

#    def __repr__(self):


# def Roku_Discover(service, timeout=2, retries=1):
