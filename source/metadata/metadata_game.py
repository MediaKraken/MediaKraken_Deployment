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
import json

from common import common_global
from common import common_logging_elasticsearch_httpx


async def game_system_update():
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    data = common_global.api_instance.com_meta_gamesdb_platform_list()[
        'Data']['Platforms']['Platform']
    print((type(data)), flush=True)
    print(data, flush=True)
    for game_system in data:
        print(game_system, flush=True)
        game_sys_detail = \
            common_global.api_instance.com_meta_gamesdb_platform_by_id(game_system['id'])['Data'][
                'Platform']
        print((type(game_sys_detail)), flush=True)
        print(game_sys_detail, flush=True)
        break


async def metadata_game_lookup(db_connection, download_data):
    """
    Lookup game metadata
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    metadata_uuid = None  # so not found checks verify later
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'game filename':
                                                                             download_data['Path']})
    # TODO determine short name/etc
    for row_data in await db_connection.db_meta_game_by_name(download_data['Path']):
        # TODO handle more than one match
        metadata_uuid = row_data['gi_id']
        break
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         "meta game metadata_uuid B": metadata_uuid})
    if metadata_uuid is None:
        # no matches by name
        # search giantbomb since not matched above via DB or nfo/xml
        await download_data.update({'Status': 'Search'})
        # save the updated status
        await db_connection.db_begin()
        await db_connection.db_download_update(json.dumps(download_data),
                                               download_data['mdq_id'])
        # set provider last so it's not picked up by the wrong thread
        await db_connection.db_download_update_provider('giantbomb', download_data['mdq_id'])
        await db_connection.db_commit()
    return metadata_uuid
