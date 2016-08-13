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

from __future__ import absolute_import, division, print_function, unicode_literals
#import logging
import os
import transmissionrpc


# transmission class
class CommonTransmission(object):
    """
    Class for interfacing with transmission bitorrent server
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.isfile("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../MediaKraken.ini")
        self.tc = transmissionrpc.Client(Config.get('Transmission', 'Host').strip(),\
            int(Config.get('Transmission', 'Port').strip()))


    def com_trans_get_torrent_list(self):
        """
        Get torrent list
        """
        return self.tc.get_torrents()


    def com_trans_add_torrent(self, torrent_path):
        """
        Add torrent by file path
        """
        #tc.add_torrent('http://releases.ubuntu.com/8.10/ubuntu-8.10-desktop-i386.iso.torrent')
        self.tc.add_torrent(torrent_path)


    def com_trans_remove_torrent(self, torrent_hash):
        """
        Remove torrent
        """
        self.tc.remove_torrent(torrent_hash)


    def com_trans_name(self, torrent_no):
        """
        Get name of torrent by id
        """
        return self.tc.get_torrent(torrent_no)


    def com_trans_torrent_detail(self, torrent_no):
        """
        Get torrent detail
        """
        torrent = self.tc.get_torrent(torrent_no)[1]
        return torrent.name, torrent.hashString, torrent.status, torrent.eta


    def com_trans_torrent_start(self, torrent_no):
        """
        Start the specified torrent
        """
        self.tc.start_torrent(torrent_no)


    def com_trans_torrent_stop(self, torrent_no):
        """
        Stop the specified torrent
        """
        self.tc.stop_torrent(torrent_no)
