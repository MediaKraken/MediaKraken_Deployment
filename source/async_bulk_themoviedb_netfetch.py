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
from common import common_network
from common import common_system


async def main(loop):
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                               message_text='START',
                                                               index_name='async_bulk_themoviedb_netfetch')

    fetch_date = '09_20_2020'

    # open the database
    option_config_json, db_connection = \
        await common_config_ini.com_config_read_async(loop=loop,
                                                      as_pool=False)

    force_dl = False
    if db_connection.db_table_count('mm_metadata_movie', db_connection=db_connection) == 0 \
            and db_connection.db_table_count('mm_download_que', db_connection=db_connection) == 0:
        force_dl = True
    # start up the range fetches for movie
    file_name = 'http://files.tmdb.org/p/exports/movie_ids_%s.json.gz' % fetch_date
    common_network.mk_network_fetch_from_url(file_name, 'movie.gz')
    json_data = common_file.com_file_ungzip('movie.gz').decode('utf-8')
    for json_row in json_data.splitlines():
        tmdb_to_fetch = str(json.loads(json_row)['id'])
        # check to see if we already have it
        if force_dl or (
                db_connection.db_meta_tmdb_count(tmdb_to_fetch, db_connection=db_connection) == 0
                and db_connection.db_download_que_exists(None,
                                                         common_global.DLMediaType.Movie.value,
                                                         'themoviedb',
                                                         str(tmdb_to_fetch),
                                                         db_connection=db_connection) is None):
            db_connection.db_download_insert(provider='themoviedb',
                                             que_type=common_global.DLMediaType.Movie.value,
                                             down_json=json.dumps({"Status": "Fetch",
                                                                   "ProviderMetaID": tmdb_to_fetch}),
                                             down_new_uuid=uuid.uuid4(),
                                             db_connection=db_connection
                                             )
    os.remove('movie.gz')

    force_dl = False
    if db_connection.db_table_count('mm_metadata_tvshow', db_connection=db_connection) == 0 \
            and db_connection.db_table_count('mm_download_que', db_connection=db_connection) == 0:
        force_dl = True
    # start up the range fetches for tv
    file_name = 'http://files.tmdb.org/p/exports/tv_series_ids_%s.json.gz' % fetch_date
    common_network.mk_network_fetch_from_url(file_name, 'tv.gz')
    json_data = common_file.com_file_ungzip('tv.gz').decode('utf-8')
    for json_row in json_data.splitlines():
        tmdb_to_fetch = str(json.loads(json_row)['id'])
        # check to see if we already have it
        if force_dl or (
                db_connection.db_meta_tmdb_count(tmdb_to_fetch, db_connection=db_connection) == 0
                and db_connection.db_download_que_exists(None,
                                                         common_global.DLMediaType.TV.value,
                                                         'themoviedb',
                                                         tmdb_to_fetch,
                                                         db_connection=db_connection) is None):
            db_connection.db_download_insert(provider='themoviedb',
                                             que_type=common_global.DLMediaType.TV.value,
                                             down_json=json.dumps({"Status": "Fetch",
                                                                   "ProviderMetaID": tmdb_to_fetch}),
                                             down_new_uuid=uuid.uuid4(),
                                             db_connection=db_connection
                                             )
    os.remove('tv.gz')

    # no reason to do the person....as the above meta will fetch them from cast/crew

    # commit all changes
    db_connection.db_commit(db_connection=db_connection)

    # close DB
    db_connection.db_close(db_connection=db_connection)

    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                               message_text='STOP')


if __name__ == "__main__":
    # verify this program isn't already running!
    if common_system.com_process_list(
            process_name='/usr/bin/python3 /mediakraken/async_bulk_themoviedb_netfetch.py'):
        sys.exit(0)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
