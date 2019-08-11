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

from steam import SteamID


# https://developer.valvesoftware.com/wiki/Steam_Web_API
class CommonNetworkSteam:
    """
    Class for interfacing with Valve Steam
    """

    def __init__(self, access_token):
        pass


def com_net_steam_id_from_user(user_name):
    return SteamID.from_url('https://steamcommunity.com/id/%s', (user_name,))
