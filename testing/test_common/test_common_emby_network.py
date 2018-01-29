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
import pytest  # pylint: disable=W0611
import sys

sys.path.append('.')
from common import common_emby_network


# https://github.com/MediaBrowser/Emby/wiki/Locating-the-Server
def test_common_network_emby_find_server():
    """
    Test function
    """
    common_emby_network.com_network_emby_find_server()

# create dictionary containing
# Name = Id, PrimaryImageTag (or NULL)
# https://github.com/MediaBrowser/Emby/wiki/Authentication
# def common_network_Emby_Find_Users(host_server):


# https://github.com/MediaBrowser/Emby/wiki/Authentication
# def common_network_Emby_User_Login(host_server, user_name, user_password):


# def common_network_Emby_User(host_server, user_id, headers):


# fetch list of open sessions for user
# def common_network_Emby_Sessions_List_Open(host_server, user_id):


# send command to specified session
# https://github.com/MediaBrowser/Emby/wiki/Remote-control
# def common_network_Emby_Sessions_Send_Command(host_server, session_id, playstate_command, session_command):


# def common_network_Emby_User_View_List(host_server, user_id, headers):


# https://github.com/MediaBrowser/Emby/wiki/Channels
# def common_network_Emby_User_Channel_List(host_server, user_id, headers):


# https://github.com/MediaBrowser/Emby/wiki/Channels
# def common_network_Emby_User_Channel_Feature_List(host_server, channel_id, headers):


# https://github.com/MediaBrowser/Emby/wiki/Channels
# def common_network_Emby_User_Channel_Items(host_server, channel_id, user_id, headers):


# https://github.com/MediaBrowser/Emby/wiki/Latest-Items
# TODO grouping and such
# TODO episodes
# def common_network_Emby_User_Latest_Items_List(host_server, request_type, request_subtype, request_limit, request_grouping, user_id, headers):


# add new sync job
# https://github.com/MediaBrowser/Emby/wiki/Sync
# def common_network_Emby_Sync_Add():


# download images
# https://github.com/MediaBrowser/Emby/wiki/Images
# def common_network_Emby_Image_Download():
# for users, the url's are /Users/{Id}/Images/{Type} and /Users/{Id}/Images/{Type}/{Index}. For media items, it's /Items/{Id}/Images/{Type}, as well as /Items/{Id}/Images/{Type}/{Index}
# TODO types
# TODO percentage complete
# TODO played or not image


# https://github.com/MediaBrowser/Emby/wiki/Items-by-name
# def common_network_Emby_Item_Info_by_Name():


# https://github.com/MediaBrowser/Emby/wiki/Playlists
# TODO create play
# TODO retrieve play
# TODO playlist items
# TODO add item to play
# TODO remove item from play

# https://github.com/MediaBrowser/Emby/wiki/Http-Live-Streaming
# TODO http stream

# https://github.com/MediaBrowser/Emby/wiki/Subtitles
# TODO grab subtitles

# https://github.com/MediaBrowser/Emby/wiki/Audio-Streaming
# TODO audio stream

# https://github.com/MediaBrowser/Emby/wiki/Video-Streaming
# TODO video stream
