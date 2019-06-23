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

import requests
import xmltodict


class CommonMetadataGamesDB:
    """
    Class for interfacing with theGamesDB
    """

    def __init__(self):
        self.BASE_URL = 'http://thegamesdb.net/api/'
        self.httpheaders = {'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'}

    def com_meta_gamesdb_platform_list(self):
        """
        Get platform list
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetPlatformsList.php',
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_platform_by_id(self, platform_id):
        """
        Platform info by id
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetPlatform.php?id=%s' % platform_id,
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_by_name(self, game_name):
        """
        # 'mega man'
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetGamesList.php?name=%s'
                                            % game_name.replace(' ', '%20'),
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_by_id(self, game_id):
        """
        # game by id
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetGamesList.php?id=%s' % game_id,
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_art_by_id(self, game_id):
        """
        # game by id
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetArt.php?id=%s' % game_id,
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_by_platform_id(self, platform_id):
        """
        Games by platform id
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'GetPlatformGames.php?platform=%s'
                                            % platform_id,
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_by_platform_name(self, platform_name):
        """
        Games by platform id
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'PlatformGames.php?platform=%s'
                                            % platform_name,
                                            verify=False, headers=self.httpheaders).text)

    def com_meta_gamesdb_games_updated_seconds(self, update_time):
        """
        Games updated in last n seconds
        """
        return xmltodict.parse(requests.get(self.BASE_URL + 'Updates.php?time=%s' % update_time,
                                            verify=False, headers=self.httpheaders).text)
