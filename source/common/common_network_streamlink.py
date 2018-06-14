'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import streamlink


# from streamlink import Streamlink, StreamError, PluginError, NoPluginError


def com_net_streamlink_streams(stream_url):
    """
    List possible streams
    """
    return streamlink.streams(stream_url)


class CommonNetworkStreamlink(object):
    """
    Class for interfacing via streamlink
    """

    def __init__(self):
        # Create the Streamlink session
        self.streamlink_inst = streamlink.Streamlink()
