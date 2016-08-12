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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from twitch.api import v3 as twitch
from twitch.scraper import get_json, download
from twitch.exceptions import ResourceUnavailableException


class CommonTwitch(object):
    """
    Class for interfacing with TwitchTV
    """
    def __init__(self):
        pass


    def MK_Common_Twitch_Get_All_Streams(self, stream_limit):
        """
        Get all streams
        """
        return twitch.streams.all(limit=stream_limit)


    def MK_Common_Twitch_Get_Featured_Streams(self):
        """
        Get featured streams
        """
        return twitch.streams.featured()


    def MK_Common_Twitch_Get_Summary(self):
        return twitch.streams.summary()


    def MK_Common_Twitch_Get_Summary_Viewers(self):
        return twitch.streams.summary().get('viewers')


    def MK_Common_Twitch_Channel_By_User(self, user_name):
        return twitch.streams.by_channel(user_name)


    def MK_Common_Twitch_By_Name(self, user_name):
        return twitch.users.by_name(user_name)


    def MK_Common_Twitch_Channel_By_Name(self, channel_name):
        return twitch.channels.by_name(channel_name)


    def MK_Common_Twitch_Get_Videos_By_Channel(self, channel_name, stream_limit):
        return twitch.channels.get_videos(channel_name, limit=stream_limit)['videos']


    def MK_Common_Twitch_Channel_Teams_By_Name(self, channel_name):
        return twitch.channels.teams(channel_name)


    def MK_Common_Twitch_Search_Channel_By_Name(self, channel_name):
        return twitch.search.channels(channel_name).get('channels')


    def MK_Common_Twitch_Search_Streams_By_Name(self, stream_game):
        return twitch.search.streams(stream_game).get('streams')


    def MK_Common_Twitch_Search_Games_By_Name(self, game_name):
        return twitch.search.games(game_name).get('games')


stuff = MK_Common_Twitch_API()
#print stuff.MK_Common_Twitch_Get_All_Streams(3)
#print stuff.MK_Common_Twitch_Get_Featured_Streams().get('featured')
#print stuff.MK_Common_Twitch_Get_Summary()
#print stuff.MK_Common_Twitch_Get_Summary_Viewers()
#print stuff.MK_Common_Twitch_Channel_By_User('winlu')
#print stuff.MK_Common_Twitch_By_Name('winlu')
#print stuff.MK_Common_Twitch_Channel_By_Name('Test_channel')
#print stuff.MK_Common_Twitch_Get_Videos_By_Channel('tornis', 5)
#print stuff.MK_Common_Twitch_Channel_Teams_By_Name('tornis')
#print stuff.MK_Common_Twitch_Search_Channel_By_Name('Test_channel')
#print stuff.MK_Common_Twitch_Search_Streams_By_Name('starcraft')
#print stuff.MK_Common_Twitch_Search_Games_By_Name('starcraft')
