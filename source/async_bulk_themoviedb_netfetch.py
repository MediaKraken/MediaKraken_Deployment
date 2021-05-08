"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

import asyncio
import json
import os
import sys
import uuid

from common import common_config_ini
from common import common_file
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network_async
from common import common_system


async def main(loop):
    # start logging
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text='START',
                                                                     index_name='async_bulk_themoviedb_netfetch')

    fetch_date = '05_05_2021'

    # open the database
    option_config_json, db_connection = \
        await common_config_ini.com_config_read_async(loop=loop,
                                                      as_pool=False)

    # start up the range fetches for movie
    file_name = 'http://files.tmdb.org/p/exports/movie_ids_%s.json.gz' % fetch_date
    # TODO handle no file!
    await common_network_async.mk_network_fetch_from_url_async(file_name, 'movie.gz')
    json_data = common_file.com_file_ungzip('movie.gz').decode('utf-8')
    for json_row in json_data.splitlines():
        tmdb_to_fetch = json.loads(json_row)
        # TODO check settings to pull down adult records
        if tmdb_to_fetch['adult']:
            pass
        # check to see if we already have it....need to do by ID as duplicate named movies, etc
        if (await db_connection.db_meta_movie_count_by_id(guid=tmdb_to_fetch['id'],
                                                          db_connection=None) is False
                and await db_connection.db_download_que_exists(download_que_uuid=None,
                                                               download_que_type=common_global.DLMediaType.Movie.value,
                                                               provider_name='themoviedb',
                                                               provider_id=tmdb_to_fetch['id'],
                                                               db_connection=None,
                                                               exists_only=True) is False):
            await db_connection.db_download_insert(provider='themoviedb',
                                                   que_type=common_global.DLMediaType.Movie.value,
                                                   down_json={"Status": "Fetch",
                                                              "ProviderMetaID":
                                                                  tmdb_to_fetch['id']},
                                                   down_new_uuid=uuid.uuid4(),
                                                   db_connection=None
                                                   )
    os.remove('movie.gz')

    # start up the range fetches for tv
    file_name = 'http://files.tmdb.org/p/exports/tv_series_ids_%s.json.gz' % fetch_date
    # TODO handle no file!
    await common_network_async.mk_network_fetch_from_url_async(file_name, 'tv.gz')
    json_data = common_file.com_file_ungzip('tv.gz').decode('utf-8')
    for json_row in json_data.splitlines():
        tmdb_to_fetch = json.loads(json_row)
        # TODO check settings to pull down adult records
        if tmdb_to_fetch['adult']:
            pass
        # check to see if we already have it....need to do by ID as duplicate named TV, etc
        if (await db_connection.db_meta_tv_count_by_id(guid=tmdb_to_fetch['id'],
                                                       db_connection=None) is False
                and await db_connection.db_download_que_exists(download_que_uuid=None,
                                                               download_que_type=common_global.DLMediaType.TV.value,
                                                               provider_name='themoviedb',
                                                               provider_id=tmdb_to_fetch['id'],
                                                               db_connection=None,
                                                               exists_only=True) is False):
            await db_connection.db_download_insert(provider='themoviedb',
                                                   que_type=common_global.DLMediaType.TV.value,
                                                   down_json={"Status": "Fetch",
                                                              "ProviderMetaID":
                                                                  tmdb_to_fetch['id']},
                                                   down_new_uuid=uuid.uuid4(),
                                                   db_connection=None
                                                   )
    os.remove('tv.gz')

    # no reason to do the person....as the above meta will fetch them from cast/crew

    # commit all changes
    await db_connection.db_commit(db_connection=None)

    # close DB
    await db_connection.db_close(db_connection=None)

    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text='STOP')


if __name__ == "__main__":
    # verify this program isn't already running!
    if common_system.com_process_list(
            process_name='/usr/bin/python3 /mediakraken/async_bulk_themoviedb_netfetch.py'):
        sys.exit(0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
