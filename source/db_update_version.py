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

import json
import subprocess

import psycopg2
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('db_update_version')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# not really needed if common_version.DB_VERSION == 4:

# if db_connection.db_version_check() == 1:
#     # add download image que
#     proc = subprocess.Popen(['python', './db_create_update.py'], shell=False)
#     proc.wait()
#     db_connection.db_version_update(2)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 2:
#     # add image for periodical
#     db_connection.db_query(
#         'ALTER TABLE mm_metadata_book ADD COLUMN mm_metadata_book_image_json jsonb')
#     db_connection.db_version_update(3)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 3:
#     # add docker info to options
#     option_config_json.update(
#         {'Docker': {'Nodes': 0, 'SwarmID': None, 'Instances': 0}})
#     db_connection.db_opt_update(option_config_json)
#     db_connection.db_version_update(4)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 4:
#     # add cron job
#     db_connection.db_cron_insert('Trailer', 'Download new trailers', False, 'Days 1',
#                                  psycopg2.Timestamp(1970, 1, 1, 0, 0, 1),
#                                  './subprogram_metadata_trailer_download.py')
#     db_connection.db_version_update(5)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 5:
#     # drop tvtuners and nas tables
#     db_connection.db_drop_table('mm_nas')
#     db_connection.db_drop_table('mm_tuner')
#     db_connection.db_version_update(6)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 6:
#     # create indexes for pg_trgm
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON mm_metadata_tvshow USING gist(mm_metadata_tvshow_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_sports_name_trigram_idx ON mm_metadata_sports USING gist(mm_metadata_sports_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_musician_name_trigram_idx ON mm_metadata_musician USING gist(mm_metadata_musician_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_album_name_trigram_idx ON mm_metadata_album USING gist(mm_metadata_album_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_music_name_trigram_idx ON mm_metadata_music USING gist(mm_metadata_music_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_media_anime_name_trigram_idx ON mm_metadata_anime USING gist(mm_media_anime_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_media_name_trigram_idx ON mm_metadata_movie USING gist(mm_media_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_media_music_video_band_trigram_idx ON mm_metadata_music_video USING gist(mm_media_music_video_band gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_media_music_video_song_trigram_idx ON mm_metadata_music_video USING gist(mm_media_music_video_song gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mm_metadata_book_name_trigram_idx ON mm_metadata_book USING gist(mm_metadata_book_name gist_trgm_ops);')
#     # since it's json, gist trgm_ops won't work
#     # db_connection.db_query('CREATE INDEX mm_metadata_collection_name_trigram_idx ON mm_metadata_collection USING gist(mm_metadata_collection_name gist_trgm_ops);')
#     db_connection.db_query(
#         'CREATE INDEX mmp_person_name_trigram_idx ON mm_metadata_person USING gist(mmp_person_name gist_trgm_ops);')
#     db_connection.db_version_update(7)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 7:
#     # drop the game audit cron
#     db_connection.db_query(
#         'delete from mm_cron where mm_cron_file_path = \'./subprogram_game_audit.py\'')
#     db_connection.db_version_update(8)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 8:
#     # drop all cron
#     db_connection.db_query('delete from mm_cron')
#     # create task tables
#     db_connection.db_query('CREATE TABLE IF NOT EXISTS mm_task (mm_task_guid uuid'
#                            ' CONSTRAINT mm_task_guid_pk PRIMARY KEY, mm_task_name text, mm_task_description text,'
#                            ' mm_task_enabled bool, mm_task_schedule text, mm_task_last_run timestamp,'
#                            ' mm_task_file_path text, mm_task_json jsonb)')
#     # create base task entries
#     base_task = [
#         # metadata
#         ('Anime', 'Match anime via Scudlee data',
#          '/mediakraken/subprogram_match_anime_id_scudlee.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'Z', 'task': 'anime'}),
#         ('Collections', 'Create and update collection(s)',
#          '/mediakraken/subprogram_metadata_update_create_collections.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'themoviedb', 'task': 'collection'}),
#         ('Create Chapter Image', 'Create chapter images for all media',
#          '/mediakraken/subprogram_create_chapter_images.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'chapter'}),
#         ('Roku Thumb', 'Generate Roku thumbnail images',
#          '/mediakraken/subprogram_roku_thumbnail_generate.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'rokuthumbnail'}),
#         ('Schedules Direct', 'Fetch TV schedules from Schedules Direct',
#          '/mediakraken/subprogram_schedules_direct_updates.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'schedulesdirect', 'task': 'update'}),
#         ('Subtitle', 'Download missing subtitles for media',
#          '/mediakraken/subprogram_subtitle_downloader.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'Z', 'task': 'subtitle'}),
#         ('The Movie Database', 'Grab updated movie metadata',
#          '/mediakraken/subprogram_metadata_tmdb_updates.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'themoviedb', 'task': 'update'}),
#         ('TheTVDB Update', 'Grab updated TheTVDB metadata',
#          '/mediakraken/subprogram_metadata_thetvdb_updates.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'thetvdb', 'task': 'update'}),
#         ('TVmaze Update', 'Grab updated TVmaze metadata',
#          '/mediakraken/subprogram_metadata_tvmaze_updates.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'tvmaze', 'task': 'update'}),
#         ('Trailer', 'Download new trailers', '/mediakraken/subprogram_metadata_trailer_download.py',
#          {'exchange_key': 'mkque_metadata_ex', 'route_key': 'Z', 'task': 'trailer'}),
#         # normal subprograms
#         ('Backup', 'Backup Postgresql DB', '/mediakraken/subprogram_postgresql_backup.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'dbbackup'}),
#         ('DB Vacuum', 'Postgresql Vacuum Analyze all tables',
#          '/mediakraken/subprogram_postgresql_vacuum.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'dbvacuum'}),
#         ('iRadio Scan', 'Scan for iRadio stations', '/mediakraken/subprogram_iradio_channels.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'iradio'}),
#         ('Media Scan', 'Scan for new media', '/mediakraken/subprogram_file_scan.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'scan'}),
#         ('Sync', 'Sync/Transcode media', '/mediakraken/subprogram_sync.py',
#          {'exchange_key': 'mkque_ex', 'route_key': 'mkque', 'task': 'sync'}),
#     ]
#     for base_item in base_task:
#         db_connection.db_task_insert(base_item[0], base_item[1], False, 'Days 1',
#                                      psycopg2.Timestamp(
#                                          1970, 1, 1, 0, 0, 1), base_item[2],
#                                      json.dumps(base_item[3]))
#     db_connection.db_version_update(9)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 9:
#     db_connection.db_query('drop table IF EXISTS mm_trigger')
#     db_connection.db_version_update(10)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 10:
#     db_connection.db_query(
#         'ALTER TABLE mm_metadata_game_software_info ADD COLUMN gi_game_info_name text')
#     db_connection.db_query(
#         'CREATE INDEX gi_game_idx_name ON mm_metadata_game_software_info(gi_game_info_name)')
#     db_connection.db_query(
#         'CREATE INDEX gi_game_idx_name_trigram_idx ON mm_metadata_game_software_info USING gist(gi_game_info_name gist_trgm_ops)')
#     db_connection.db_version_update(11)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 11:
#     db_connection.db_query(
#         'ALTER TABLE mm_metadata_game_software_info ADD COLUMN gi_game_info_short_name text')
#     db_connection.db_query(
#         'CREATE INDEX gi_game_idx_short_name ON mm_metadata_game_software_info(gi_game_info_short_name)')
#     db_connection.db_query(
#         'CREATE INDEX gi_game_idx_short_name_trigram_idx ON mm_metadata_game_software_info USING gist(gi_game_info_short_name gist_trgm_ops)')
#     db_connection.db_version_update(12)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 12:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json.update(
#         {'API': {'openweathermap': '575b4ae4615e4e2a4c34fb9defa17ceb'}})
#     db_connection.db_opt_update(options_json)
#     db_connection.db_version_update(13)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 13:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json.update({'API': {'soundcloud': None}})
#     db_connection.db_opt_update(options_json)
#     db_connection.db_version_update(14)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 14:
#     db_connection.db_query(
#         'ALTER TABLE mm_metadata_game_software_info DROP COLUMN gs_game_system_id')
#     db_connection.db_version_update(15)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 15:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json.update({'API': {'shoutcast': None}})
#     db_connection.db_opt_update(options_json)
#     db_connection.db_version_update(16)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 16:
#     db_connection.db_query('drop table mm_download_image_que')
#     db_connection.db_version_update(17)
#     db_connection.db_commit()
#
# if db_connection.db_version_check() == 17:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json.update({'Docker Instances': {'mumble': False, 'musicbrainz': False,
#                                               'portainer': False, 'smtp': False,
#                                               'teamspeak': False, 'transmission': False}})
#     db_connection.db_opt_update(options_json)
#     db_connection.db_version_update(18)
#     db_connection.db_commit()

########### all before this are historical at this point

if db_connection.db_version_check() == 19:
    # hardware device (receivers, etc, for remote control)
    db_connection.db_query('create table IF NOT EXISTS mm_hardware (mm_hardware_id uuid'
                           ' CONSTRAINT mm_hardware_id primary key, mm_hardware_manufacturer text,'
                           ' mm_hardware_model text, mm_hardware_json jsonb)')
    if db_connection.db_table_index_check('mm_hardware_idx_manufacturer') is None:
        db_connection.db_query(
            'CREATE INDEX mm_hardware_idx_manufacturer ON mm_hardware(mm_hardware_manufacturer)')
    if db_connection.db_table_index_check('mm_hardware_idx_model') is None:
        db_connection.db_query(
            'CREATE INDEX mm_hardware_idx_model ON mm_hardware(mm_hardware_model)')
    db_connection.db_version_update(20)
    db_connection.db_commit()

# if db_connection.db_version_check() == 20:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json.update({'Docker Instances': {'wireshark': False}})
#     db_connection.db_opt_update(options_json)
#     db_connection.db_version_update(21)
#     db_connection.db_commit()

# close the database
db_connection.db_close()
