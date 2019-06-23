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

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_network_telnet


class TestCommonTelnet:

    @classmethod
    def setup_class(self):
        self.telnet_connection = common_network_telnet.CommonNetworkTelnet()

    @classmethod
    def teardown_class(self):
        pass

    @pytest.mark.parametrize(("telnet_host", "telnet_port", "telnet_user", "telnet_password"), [
        ('', 'spootdevfake@gmail.com', "test1", "body"),
        ('', 'spootdev@gmail.com', "test2", "body"),
        ('', 'spootdev@fakegmail.com', "test3", "body")])
    def test_com_net_telnet_open_device(self, telnet_host, telnet_port, telnet_user,
                                        telnet_password):
        self.test_device = common_network_telnet.CommonNetworkTelnet(telnet_host, telnet_port,
                                                                     telnet_user,
                                                                     telnet_password)

    def test_com_net_telnet_read_device(self):
        """
        Test function
        """
        self.test_device.com_net_telnet_read_device()

    def test_com_net_telnet_write_device(self):
        """
        Test function
        """
        self.test_device.com_net_telnet_write_device("Telnet test message")
