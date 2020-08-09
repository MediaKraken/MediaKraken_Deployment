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

# https://github.com/MediaKraken-Dependancies/python-twitch-client
from twitch import TwitchClient


class CommonNetworkTwitchV5:
    """
    Class for interfacing with TwitchTV V5 api
    """

    def __init__(self, option_config_json):
        self.twitch_inst = TwitchClient(client_id=option_config_json['Twitch']['ClientID'],
                                        oauth_token=option_config_json['Twitch']['OAuth'])

    # chat
    def com_net_twitch_chat_badges(self, channel_id):
        return self.twitch_inst.get_badges_by_channel(channel_id)

    def com_net_twitch_chat_emoticons(self):
        return self.twitch_inst.get_all_emoticons()

    # channel feed

    # channels
    def com_net_twitch_channels_by_id(self, channel_id):
        """
        Gets a specified channel object.
        Parameters: channel_id (string) - Channel ID
        """
        return self.twitch_inst.channels.get_by_id(channel_id)

    # clips
    def com_net_twitch_clip_by_slug(self, slug_id):
        """
        Gets a clip object based on the slug provided
        Parameters: slug (string) - Twitch Slug.
        """
        return self.twitch_inst.clips.get_by_slug(slug_id)

    def com_net_twitch_top_channels(self, channel, cursor, game, language, limit, period, trending):
        """
        channel (string) – Channel name. If this is specified, top clips for only this channel are returned; otherwise, top clips for all channels are returned. If both channel and game are specified, game is ignored.
        cursor (string) – Tells the server where to start fetching the next set of results, in a multi-page response.
        game (string) – Game name. (Game names can be retrieved with the Search Games endpoint.) If this is specified, top clips for only this game are returned; otherwise, top clips for all games are returned. If both channel and game are specified, game is ignored.
        language (string) – Comma-separated list of languages, which constrains the languages of videos returned. Examples: es, en,es,th. If no language is specified, all languages are returned.
        limit (int) – Maximum number of most-recent objects to return. Default: 10. Maximum: 100.
        period (string) – The window of time to search for clips. Valid values: day, week, month, all. Default: week.
        trending (boolean) – If True, the clips returned are ordered by popularity; otherwise, by viewcount. Default: False.
        """
        return self.twitch_inst.get_top()

    def com_net_twitch_followed(self, limit, cursor, trending):
        """
        limit (int) – Maximum number of most-recent objects to return. Default: 10. Maximum: 100.
        cursor (string) – Tells the server where to start fetching the next set of results, in a multi-page response.
        trending (boolean) – If true, the clips returned are ordered by popularity; otherwise, by viewcount. Default: false.
        """
        return self.twitch_inst.followed()

    # communities

    # collections

    # games

    # ingests

    # search

    # streams

    def com_net_twitch_get_featured(self, limit=100, offset=0):
        return self.twitch_inst.get_featured(limit, offset)

    # teams

    # users

    # videos
