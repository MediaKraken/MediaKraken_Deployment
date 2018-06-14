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

from twitch.api import v3 as twitch


# from twitch.scraper import get_json, download
# from twitch.exceptions import ResourceUnavailableException


class CommonNetworkTwitch(object):
    """
    Class for interfacing with TwitchTV
    """

    def __init__(self):
        pass

    def com_twitch_get_all_streams(self, stream_limit):
        """
        Get all streams
        """
        return twitch.streams.all(limit=stream_limit)

    def com_twitch_get_featured_streams(self):
        """
        Get featured streams
        """
        return twitch.streams.featured()

    def com_twitch_get_summary(self):
        """
        Get summary
        """
        return twitch.streams.summary()

    def com_twitch_get_summary_viewers(self):
        """
        Get veiwers of summary
        """
        return twitch.streams.summary().get('viewers')

    def com_twitch_channel_by_user(self, user_name):
        """
        Get user channels
        """
        return twitch.streams.by_channel(user_name)

    def com_twitch_by_name(self, user_name):
        """
        Get data by user name
        """
        return twitch.users.by_name(user_name)

    def com_twitch_channel_by_name(self, channel_name):
        """
        Grab info by channel name
        """
        return twitch.channels.by_name(channel_name)

    def com_twitch_get_videos_by_channel(self, channel_name, stream_limit):
        """
        Search videos by channel name
        """
        return twitch.channels.get_videos(channel_name, limit=stream_limit)['videos']

    def com_twitch_channel_teams_by_name(self, channel_name):
        """
        Get teams by channel name
        """
        return twitch.channels.teams(channel_name)

    def com_twitch_search_channel_by_name(self, channel_name):
        """
        Search by channel name
        """
        return twitch.search.channels(channel_name).get('channels')

    def com_twitch_search_streams_by_name(self, stream_game):
        """
        Search streams by game name
        """
        return twitch.search.streams(stream_game).get('streams')

    def com_twitch_search_games_by_name(self, game_name):
        """
        Search games by name
        """
        return twitch.search.games(game_name).get('games')

# stuff = CommonNetworkTwitch()
# print stuff.com_twitch_get_all_streams(3)
# print stuff.com_twitch_get_Featured_Streams().get('featured')
# print stuff.com_twitch_get_Summary()
# print stuff.com_twitch_get_Summary_Viewers()
# print stuff.com_twitch_channel_by_User('winlu')
# print stuff.com_twitch_by_Name('winlu')
# print stuff.com_twitch_channel_by_Name('test_channel')
# print stuff.com_twitch_get_Videos_by_Channel('tornis', 5)
# print stuff.com_twitch_channel_Teams_by_Name('tornis')
# print stuff.com_twitch_search_Channel_by_Name('test_channel')
# print stuff.com_twitch_search_Streams_by_Name('starcraft')
# print stuff.com_twitch_search_Games_by_Name('starcraft')
