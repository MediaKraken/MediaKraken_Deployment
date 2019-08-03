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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_network_twitch


class TestCommonTwitch:

    @classmethod
    def setup_class(self):
        self.twitch_connection = common_network_twitch.CommonNetworkTwitch()

    @classmethod
    def teardown_class(self):
        pass

    @pytest.mark.parametrize(("stream_limit"), [
        (0),
        (5)])
    def test_com_Twitch_Get_All_Streams(self, stream_limit):
        """
        Test function
        """
        self.twitch_connection.com_twitch_get_all_streams(stream_limit)

    def test_com_Twitch_Get_Featured_Streams(self):
        """
        Test function
        """
        self.twitch_connection.com_twitch_get_featured_streams()

    def test_com_Twitch_Get_Summary(self):
        """
        Test function
        """
        self.twitch_connection.com_twitch_get_summary()

    def test_com_Twitch_Get_Summary_Viewers(self):
        """
        Test function
        """
        self.twitch_connection.com_twitch_get_summary_viewers()

#    def com_Twitch_Channel_by_User(self, user_name):


#    def com_Twitch_by_Name(self, user_name):


#    def com_Twitch_Channel_by_Name(self, channel_name):


#    def com_Twitch_Get_Videos_by_Channel(self, channel_name, stream_limit):


#    def com_Twitch_Channel_Teams_by_Name(self, channel_name):


#    def com_Twitch_Search_Channel_by_Name(self, channel_name):


#    def com_Twitch_Search_Streams_by_Name(self, stream_game):


#    def com_Twitch_Search_Games_by_Name(self, game_name):
