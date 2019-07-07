'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# https://github.com/MediaKraken-Dependancies/python-tidal
import tidalapi


class CommonNetworkTidal:
    """
    Class for interfacing with Tidal
    """

    def __init__(self, user_name, user_password):
        self.session = tidalapi.Session()
        self.session.login(user_name, user_password)

    def com_net_tidal_get_tracks(self, album_id):
        return self.session.get_album_tracks(album_id=album_id)
