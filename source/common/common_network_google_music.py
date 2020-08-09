"""
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
"""

# https://unofficial-google-music-api.readthedocs.io/en/latest/
from gmusicapi import Mobileclient


class CommonNetworkGoogleMusic:
    """
    Class for interfacing with google music
    """

    def __init__(self, api_user, api_password):
        self.api_inst = Mobileclient()
        self.api_inst.login(api_user, api_password, Mobileclient.FROM_MAC_ADDRESS)

    def com_net_google_music_all_songs(self):
        return self.api_inst.get_all_songs()

    def com_net_google_music_create_playlist(self, playlist_name):
        # returns playlist id
        return self.api_inst.create_playlist(playlist_name)

    def com_net_google_music_add_to_playlist(self, playlist_id, track_ids):
        self.api_inst.add_songs_to_playlist(playlist_id, track_ids)

    def com_net_google_music_song_url(self, song_id):
        return self.api_inst.get_stream_url(song_id, device_id=None, quality='hi')

    def com_net_google_music_logout(self):
        self.api_inst.logout()

# sweet_track_ids = [track['id'] for track in library if track['artist'] == 'The Cat Empire']
