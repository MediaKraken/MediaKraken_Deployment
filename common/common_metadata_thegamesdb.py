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
from gamesdb.api import API

'''
Game
    id
    title
    release_date
    platform
    overview
    esrb_rating
    genres
    players
    coop
    youtube_url
    publisher
    developer
    rating
    logo_url

Platform
    id
    name
    alias
    console
    controller
    overview
    developer
    manufacturer
    cpu
    memory
    graphics
    sound
    display
    media
    max_controllers
    rating
'''

# setup class so I don't define the api resource unless I'm doing a lookup
class CommonMetadataGamesDB(object):
    """
    Class for interfacing with GamesDB
    """
    def __init__(self):
        self.gamesdb_api = API()


    def MK_Common_Metadata_GamesDB_Platform_List(self):
        """
        Get platform list
        """
        platform_list = self.gamesdb_api.get_platforms_list()
        for platform in platform_list:
            print(platform.id, "-", platform.name, "-", platform.alias)
        return platform_list


    def MK_Common_Metadata_GamesDB_Platform_By_ID(self, platform_id):
        """
        Platform info by id
        """
        game_platform = self.gamesdb_api.get_platform(platform_id)
        print(game_platform.name)
        print(game_platform.overview)
        return game_platform


    def MK_Common_Metadata_GamesDB_Games_By_Name_Or(self, game_name):
        """
        # 'mega man' as mega OR man
        """
        for game in self.gamesdb_api.get_game(name=game_name):
            print(game.title)
            print(game.platform)
            print(game.release_date)


    def MK_Common_Metadata_GamesDB_Games_By_Name_And(self, game_name):
        """
        # 'mega man' as mega AND man
        """
        for game in self.gamesdb_api.get_games_list(name=game_name):
            print(game.title)
            print(game.platform)
            print(game.release_date)


    def MK_Common_Metadata_GamesDB_Games_By_Name_And_Platform_Or(self, game_name, platform_name,\
            game_genre=None):
        """
        Fetch games by name OR platform
        """
        for game in self.gamesdb_api.get_game(name=game_name, platform=platform_name,\
                genre=game_genre):
            print(game.title)
            print(game.platform)


    def MK_Common_Metadata_GamesDB_Games_By_Name_And_Platform_And(self, game_name, platform_name,\
            game_genre=None):
        """
        Fetch games by name AND platform
        """
        for game in self.gamesdb_api.get_games_list(name=game_name, platform=platform_name,\
                genre=game_genre):
            print(game.title)
            print(game.platform)


    def MK_Common_Metadata_GamesDB_Games_By_Platform_ID(self, platform_id):
        """
        Games by platform id
        """
        for game in self.gamesdb_api.get_platform_games(platform_id):
            print(game.id, "-", game.title, "-", game.release_date)


    def MK_Common_Metadata_GamesDB_Games_By_ID(self, game_id):
        """
        Games by game id
        """
        game = self.gamesdb_api.get_game(id=game_id)
        print(game.title)
        print(game.overview)
        print(game.genres)
        print(game.developer)
        return game
