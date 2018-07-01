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

# https://github.com/MediaKraken-Dependancies/pylast
import pylast


class CommonMetadataLastFM(object):
    """
    Class for interfacing with lastfm
    """

    def __init__(self, option_config_json):
        self.lastfm_inst = pylast.LastFMNetwork(api_key=option_config_json['LastFM']['api_key'],
                                                api_secret=option_config_json['LastFM'][
                                                    'api_secret'],
                                                username=option_config_json['LastFM']['username'],
                                                password_hash=option_config_json['LastFM'][
                                                    'password'])

        # # Now you can use that object everywhere
        # artist = network.get_artist("System of a Down")
        # artist.shout("<3")
        #
        #
        # track = network.get_track("Iron Maiden", "The Nomad")
        # track.love()
        # track.add_tags(("awesome", "favorite"))
        #
        # # Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
        # # to get more help about anything and see examples of how it works
