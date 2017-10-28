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
from pylms.server import Server
from pylms.player import Player


class CommonNetLMS(object):
    def __init__(self, hostname="192.168.1.1", port=9090, username="user",
                 password="password"):
        self.lms_device = Server(hostname=hostname, port=port,
                                 username=username, password=password)
        self.lms_device.connect()

    def com_net_lms_version(self):
        return self.lms_device.get_version()

    def com_net_lms_logged_in(self):
        return self.lms_device.logged_in

    def com_net_lms_status(self):
        sq = self.lms_device.get_player("00:11:22:33:44:55")
        return sq.get_name(), sq.get_mode(), sq.get_time_elapsed(), sq.is_connected,\
            sq.get_wifi_signal_strength(), sq.get_track_title(), sq.get_time_remaining()
