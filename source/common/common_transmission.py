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

import transmissionrpc


# transmission class
class CommonTransmission:
    """
    Class for interfacing with transmission bitorrent server
    """

    def __init__(self, option_config_json):
        self.trans_connection = transmissionrpc.Client(
            option_config_json['Transmission']['Host'],
            int(option_config_json['Transmission']['Port']))

    def com_trans_get_torrent_list(self):
        """
        Get torrent list
        """
        return self.trans_connection.get_torrents()

    def com_trans_add_torrent(self, torrent_path):
        """
        Add torrent by file path
        """
        # trans_connection.add_torrent('http://releases.ubuntu.com/8.10/i386.iso.torrent')
        self.trans_connection.add_torrent(torrent_path)

    def com_trans_remove_torrent(self, torrent_hash):
        """
        Remove torrent
        """
        self.trans_connection.remove_torrent(torrent_hash)

    def com_trans_name(self, torrent_no):
        """
        Get name of torrent by id
        """
        return self.trans_connection.get_torrent(torrent_no)

    def com_trans_torrent_detail(self, torrent_no):
        """
        Get torrent detail
        """
        torrent = self.trans_connection.get_torrent(torrent_no)[1]
        return torrent.name, torrent.hashString, torrent.status, torrent.eta

    def com_trans_torrent_start(self, torrent_no):
        """
        Start the specified torrent
        """
        self.trans_connection.start_torrent(torrent_no)

    def com_trans_torrent_stop(self, torrent_no):
        """
        Stop the specified torrent
        """
        self.trans_connection.stop_torrent(torrent_no)
