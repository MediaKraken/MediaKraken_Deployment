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


# grab the updated data
tmdb = common_metadata_tmdb.CommonMetadataTMDB(option_config_json)

# process movie changes
for movie_change in tmdb.com_tmdb_meta_changes_movie()['results']:
    logging.debug("mov: %s", movie_change['id'])
    dl_meta = db_connection.db_download_que_exists(None, 'themoviedb', str(movie_change['id']))
    if dl_meta is None:
        db_connection.db_download_insert('themoviedb', json.dumps({'MediaID': None,\
            'Path': None, 'ClassID': None, 'Status': 'Fetch',\
            'MetaNewID': None, 'ProviderMetaID': str(movie_change['id'])}))

# process tv changes
for tv_change in tmdb.com_tmdb_meta_changes_tv()['results']:
    logging.debug("tv: %s", tv_change['id'])
    dl_meta = db_connection.db_download_que_exists(None, 'themoviedb', str(tv_change['id']))
    if dl_meta is None:
        db_connection.db_download_insert('themoviedb', json.dumps({'MediaID': None,\
            'Path': None, 'ClassID': None, 'Status': 'Fetch',\
            'MetaNewID': None, 'ProviderMetaID': str(tv_change['id'])}))


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
    db_connection.db_trigger_insert((\
        'subprogram_update_create_collections'))


# commit all changes
db_connection.db_commit()


# close DB
db_connection.db_close()
