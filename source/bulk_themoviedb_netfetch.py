'''
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
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import uuid
import json
from common import common_config_ini
from common import common_metadata_tmdb

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# verify themoviedb key exists
if option_config_json['API']['themoviedb'].strip() != 'None':
    # setup the thmdb class
    TMDB_API_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB(
        option_config_json)
    print("Using key %s", option_config_json['API']['themoviedb'].strip())
else:
    TMDB_API_CONNECTION = None
    print("API not available.")

if TMDB_API_CONNECTION is not None:
    # start up the range fetches for movie
    for tmdb_to_fetch in range(1, TMDB_API_CONNECTION.com_tmdb_metadata_id_max()):
        # check to see if we already have it
        if db_connection.db_meta_tmdb_count(tmdb_to_fetch) == 0 \
                and db_connection.db_download_que_exists(None, 1, 'themoviedb',
                                                         str(tmdb_to_fetch)) is None:
            db_connection.db_download_insert('themoviedb', 1, json.dumps({"Status": "Fetch",
                                                                          "ProviderMetaID": str(
                                                                              tmdb_to_fetch),
                                                                          "MetaNewID": str(
                                                                              uuid.uuid4())}))

    # # start up the range fetchs for tv
    # for tmdb_to_fetch in range(1, TMDB_API_CONNECTION.com_tmdb_metadata_tv_id_max()):
    #     # check to see if we already have it
    #     if db_connection.db_meta_tmdb_count(tmdb_to_fetch) == 0 \
    #             and db_connection.db_download_que_exists(None, 2, 'themoviedb',
    #             str(tmdb_to_fetch)) is None:
    #         db_connection.db_download_insert('themoviedb', 2,
    #                                          json.dumps({"Status": "Fetch",
    #                                          "ProviderMetaID": str(tmdb_to_fetch),
    #                                          "MetaNewID": str(uuid.uuid4())}))

    # no reason to do the person....and the above meta will fetch them from cast/crew
    # # start up the range fetchs for person
    # for tmdb_to_fetch in range(1, TMDB_API_CONNECTION.com_tmdb_metadata_bio_id_max()):
    #     if JUST_DO_IT:
    #         db_connection.db_download_insert('themoviedb', 3, json.dumps({"Status": "Fetch",
    #             "ProviderMetaID": str(tmdb_to_fetch), "MetaNewID": str(uuid.uuid4())}))
    #     else:
    #         # check to see if we already have it
    #         if db_connection.db_meta_tmdb_bio_count(tmdb_to_fetch) == 0 \
    #                 and db_connection.db_download_que_exists(None, 3, 'themoviedb',
    #                 str(tmdb_to_fetch)) is None:
    #             db_connection.db_download_insert('themoviedb', 3,
    #                                              json.dumps({"Status": "Fetch",
    #                                              "ProviderMetaID": str(tmdb_to_fetch),
    #                                              "MetaNewID": str(uuid.uuid4())}))

# commit all changes
db_connection.db_commit()

# vaccuum
db_connection.db_pgsql_vacuum_table('mm_download_que')

# close DB
db_connection.db_close()
