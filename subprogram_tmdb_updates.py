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
import logging # pylint: disable=W0611
import json
import uuid
import locale
locale.setlocale(locale.LC_ALL, '')
from common import common_config_ini
from common import common_logging
from common import common_metadata_tmdb
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_TMDB_Updates')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server TMDB Update Start', None,\
    'System: Server TMDB Start', 'ServertheTMDBStart', None, None, 'System')


# grab the data
tvshow_updated = 0
tvshow_inserted = 0
movie_updated = 0
movie_inserted = 0


def movie_fetch_save(tmdb_id):
    """
    # fetch from tmdb
    """
    metadata_uuid = None
    logging.debug("fetch: %s", tmdb_id)
    # fetch and save json data via tmdb id
    result_json = tmdb.com_tmdb_meta_by_id(tmdb_id)
    if result_json is not None:
        logging.debug("here I am")
        series_id_json, result_json, image_json = tmdb.com_tmdb_meta_info_build(result_json)
        cast_json = tmdb.com_tmdb_meta_cast_by_id(tmdb_id)
        # set and insert the record
        meta_json = ({'Meta': {'TMDB': {'Meta': result_json, 'Cast': cast_json['cast'],\
            'Crew': cast_json['crew']}}})
        # check for previous record
        if db_connection.db_meta_tmdb_count(result_json['id']) > 0:
            # TODO if this is > 0......MUST use series id from DB.......so, stuff doesn't get wiped
            #db_connection.db_meta_update(series_id_json, result_json['title'],
        #json.dumps(meta_json), json.dumps(image_json))
            pass
        else:
            # store person info
            if 'cast' in cast_json:
                db_connection.db_meta_person_insert_cast_crew('TMDB', cast_json['cast'])
            if 'crew' in cast_json:
                db_connection.db_meta_person_insert_cast_crew('TMDB', cast_json['crew'])
            # grab reviews
            review_json = tmdb.com_tmdb_meta_review_by_id(tmdb_id)
            if review_json['total_results'] > 0:
                review_json_id = ({'TMDB': str(review_json['id'])})
                logging.debug("review: %s", review_json_id)
                db_connection.db_review_insert(json.dumps(review_json_id),\
                    json.dumps({'TMDB': review_json}))
            # set and insert the record
            metadata_uuid = str(uuid.uuid4())
            db_connection.db_meta_insert_tmdb(metadata_uuid, series_id_json,\
                result_json['title'], json.dumps(meta_json), json.dumps(image_json))
    return metadata_uuid


# grab the updated data
tmdb = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)
for movie_change in tmdb.com_tmdb_meta_changes_movie()['results']:
    logging.debug("mov: %s", movie_change['id'])
    movie_fetch_save(movie_change['id'])
for tv_change in tmdb.com_tmdb_meta_changes_tv()['results']:
    logging.debug("tv: %s", tv_change['id'])
    movie_fetch_save(tv_change['id'])


# log end
db_connection.db_activity_insert('MediaKraken_Server TMDB Update Stop', None,\
    'System: Server TMDB Stop', 'ServertheTMDBStop', None, None, 'System')


create_collection_trigger = False
# send notications
if tvshow_updated > 0:
    db_connection.db_notification_insert(locale.format('%d', tvshow_updated, True)\
        + " TV show(s) metadata updated.", True)
    create_collection_trigger = True
if tvshow_inserted > 0:
    db_connection.db_notification_insert(locale.format('%d', tvshow_inserted, True)\
        + " TV show(s) metadata added.", True)
    create_collection_trigger = True
if movie_updated > 0:
    db_connection.db_notification_insert(locale.format('%d', movie_updated, True)\
        + " movie metadata updated.", True)
    create_collection_trigger = True
if movie_inserted > 0:
    db_connection.db_notification_insert(locale.format('%d', movie_inserted, True)\
        + " movie metadata added.", True)
    create_collection_trigger = True
# update collection
if create_collection_trigger:
    db_connection.db_trigger_insert(('python',\
        './subprogram_update_create_collections.py'))


# commit all changes
db_connection.db_commit()


# close DB
db_connection.db_close()
