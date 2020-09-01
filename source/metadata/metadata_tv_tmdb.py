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

import json
import time

import psycopg2
from common import common_global


def tv_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid):
    """
    # tmdb data fetch for tv
    """
    common_global.es_inst.com_elastic_index('info', {"meta tv themoviedb save fetch": tmdb_id})
    result_json = common_global.api_instance.com_tmdb_metadata_tv_by_id(tmdb_id)
    common_global.es_inst.com_elastic_index('info', {'tv fetch save themoviedb show': result_json})
    # 504	Your request to the backend server timed out. Try again.
    if result_json is None or result_json.status_code == 504:
        time.sleep(60)
        # redo fetch due to 504
        tv_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 200:
        series_id, result_json, image_json \
            = common_global.api_instance.com_tmdb_meta_info_build(result_json.json())
        common_global.es_inst.com_elastic_index('info', {"series": series_id})
        # set and insert the record
        try:
            db_connection.db_metatv_insert_tmdb(metadata_uuid,
                                                series_id,
                                                result_json['name'],
                                                json.dumps(result_json),
                                                json.dumps(image_json))
            # store the cast and crew
            if 'credits' in result_json:  # cast/crew doesn't exist on all media
                if 'cast' in result_json['credits']:
                    db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                  result_json['credits']['cast'])
                if 'crew' in result_json['credits']:
                    db_connection.db_meta_person_insert_cast_crew('themoviedb',
                                                                  result_json['credits']['crew'])
        # this except is to check duplicate keys for mm_metadata_pk
        except psycopg2.IntegrityError:
            # TODO technically I could be missing cast/crew
            #  if the above doesn't finish after the insert
            pass
    # 429	Your request count (#) is over the allowed limit of (40).
    elif result_json.status_code == 429:
        time.sleep(20)
        # redo fetch due to 504
        tv_fetch_save_tmdb(db_connection, tmdb_id, metadata_uuid)
    elif result_json.status_code == 404:
        # TODO handle 404's better
        metadata_uuid = None
    else:  # is this is None....
        metadata_uuid = None
    return metadata_uuid
