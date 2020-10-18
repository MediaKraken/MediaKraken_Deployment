"""
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
"""

import inspect
import httpx
import xmltodict
from common import common_logging_elasticsearch_httpx


class CommonMetadataGamesDB:
    """
    Class for interfacing with theGamesDB
    """

    def __init__(self, option_config_json):
        self.BASE_URL = 'http://thegamesdb.net/api/'
        self.httpheaders = {'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'}

    async def com_meta_gamesdb_platform_list(self):
        """
        Get platform list
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetPlatformsList.php',
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_platform_by_id(self, platform_id):
        """
        Platform info by id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetPlatform.php?id=%s' % platform_id,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_by_name(self, game_name):
        """
        # 'mega man'
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetGamesList.php?name=%s'
                                                    % game_name.replace(' ', '%20'),
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_by_id(self, game_id):
        """
        # game by id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetGamesList.php?id=%s' % game_id,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_art_by_id(self, game_id):
        """
        # game by id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetArt.php?id=%s' % game_id,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_by_platform_id(self, platform_id):
        """
        Games by platform id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'GetPlatformGames.php?platform=%s'
                                                    % platform_id,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_by_platform_name(self, platform_name):
        """
        Games by platform id
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'PlatformGames.php?platform=%s'
                                                    % platform_name,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))

    async def com_meta_gamesdb_games_updated_seconds(self, update_time):
        """
        Games updated in last n seconds
        """
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'function':
                                                                                 inspect.stack()[0][
                                                                                     3],
                                                                             'locals': locals(),
                                                                             'caller':
                                                                                 inspect.stack()[1][
                                                                                     3]})
        async with httpx.AsyncClient() as client:
            return xmltodict.parse(await client.get(self.BASE_URL + 'Updates.php?time=%s' % update_time,
                                                    headers=self.httpheaders,
                                                    timeout=3.05))
