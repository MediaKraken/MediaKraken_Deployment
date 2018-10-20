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

# https://github.com/MediaKraken-Dependancies/python-twitch-client
from twitch import TwitchClient


class CommonNetworkTwitchV5(object):
    """
    Class for interfacing with TwitchTV V5 api
    """

    def __init__(self, client_api_id, client_oauth=None):
        if client_oauth is None:
            self.twitch_inst = TwitchClient(client_api_id)
        else:
            self.twitch_inst = TwitchClient(client_api_id, client_oauth)

    # chat

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

        # get_top(channel, cursor, game, language, limit, period, trending
        # followed()

    # communities

    # collections

    # games

    # ingests

    # search

    # streams

    # teams

    # users

    # videos
