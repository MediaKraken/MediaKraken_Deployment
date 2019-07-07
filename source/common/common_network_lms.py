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

from pylms.server import Server


class CommonNetLMS:
    def __init__(self, hostname="192.168.1.1", port=9090, username="user",
                 password="password"):
        self.lms_device = Server(hostname=hostname, port=port,
                                 username=username, password=password)
        self.lms_device.connect()

    def com_net_lms_version(self):
        return self.lms_device.get_version()

    def com_net_lms_logged_in(self):
        return self.lms_device.logged_in

    def com_net_lms_close(self):
        self.lms_device.disconnect()

    def com_net_lms_play_count(self):
        return self.lms_device.get_player_count()

    def com_net_lms_get_players(self, update=True):
        return self.lms_device.get_players(update=update)

    def com_net_lms_connect(self):
        self.lms_device.login()

    def com_net_lms_request(self, command_string, preserve_encoding=False):
        self.lms_device.request(
            command_string, preserve_encoding=preserve_encoding)

    def com_net_lms_request_results(self, command_string, preserve_encoding=False):
        self.lms_device.request_with_results(
            command_string, preserve_encoding=preserve_encoding)

    def com_net_lms_rescan(self, mode='fast'):
        # ‘fast’ for update changes on library, ‘full’ for complete library scan
        #  and ‘playlists’ for playlists scan only
        self.lms_device.rescan(mode=mode)

    def com_net_lms_rescanprogress(self):
        self.lms_device.rescanprogress()

    def com_net_lms_search(self, search_term, mode='albums'):
        self.lms_device.search(search_term, mode=mode)

    def com_net_lms_telnet_connect(self):
        self.lms_device.telnet_connect()
