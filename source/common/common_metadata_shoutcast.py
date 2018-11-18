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

import json

from . import common_network


class CommonMetadataShoutcast(object):
    """
    Class for interfacing with Shoutcast
    """

    def __init__(self, option_config_json):
        self.shoutcast_api_key = option_config_json['API']['shoutcast']
        self.shoutcast_url = 'http://api.shoutcast.com/legacy/'

    def com_shoutcast_generate_options(self, rec_limit=None, bit_rate=None, media_type=None):
        options = ''
        if rec_limit is not None:
            options += '&limit=%s' % rec_limit
        if bit_rate is not None:
            options += '&br=%s' % bit_rate
        if media_type is not None:
            # MP3 = audio/mpeg and AAC+ = audio/aacp
            if media_type.lower() == 'mp3':
                media_type = 'audio/mpeg'
            else:
                media_type = 'audio/aacp'
            options += '&mt=%s' % media_type
        return options

    def com_shoutcast_top_500(self, rec_limit=None, bit_rate=None, media_type=None):
        """
        Grab top 500 stations
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            self.shoutcast_url + 'Top500?k=' + self.shoutcast_api_key
            + self.com_shoutcast_generate_options(rec_limit, bit_rate, media_type), None))

    def com_shoutcast_keyword(self, search_string, rec_limit=None, bit_rate=None, media_type=None):
        """
        Grab stations by keyword
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            self.shoutcast_url + 'stationsearch?k=' + self.shoutcast_api_key
            + ('&search=%s' % search_string.replace(' ', '+'))
            + self.com_shoutcast_generate_options(rec_limit, bit_rate, media_type), None))

    def com_shoutcast_genre(self, genre_string, rec_limit=None, bit_rate=None, media_type=None):
        """
        Grab stations by genre
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            self.shoutcast_url + 'stationsearch?k=' + self.shoutcast_api_key
            + ('&genresearch=%s' % genre_string.replace(' ', '+'))
            + self.com_shoutcast_generate_options(rec_limit, bit_rate, media_type), None))

    def com_shoutcast_genre_list(self):
        """
        Grab genre list
        """
        return json.loads(common_network.mk_network_fetch_from_url(
            self.shoutcast_url + 'genrelist?k=' + self.shoutcast_api_key, None))

# TODO
# Get Secondary Genres
