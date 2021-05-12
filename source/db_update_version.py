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

import datetime
import json

from common import common_config_ini
from common import common_logging_elasticsearch_httpx

dont_force_localhost = True

if dont_force_localhost:
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='START',
                                                         index_name='db_update_version')
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read(force_local=False)
else:
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read(force_local=True)

# not really needed if common_version.DB_VERSION == 4:

# if db_connection.db_version_check() == 1:
#     # add download image que
#     proc = subprocess.Popen(['python', './db_create_update.py'], stdout=subprocess.PIPE, shell=False)
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
#                                  datetime.datetime(1970, 1, 1, 0, 0, 1),
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
#          '/mediakraken/async_metadata_themoviedb_updates.py',
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

# if db_connection.db_version_check() == 19:
#     # hardware device (receivers, etc, for remote control)
#     db_connection.db_query('create table IF NOT EXISTS mm_hardware (mm_hardware_id uuid'
#                            ' CONSTRAINT mm_hardware_id primary key, mm_hardware_manufacturer text,'
#                            ' mm_hardware_model text, mm_hardware_json jsonb)')
#     if db_connection.db_table_index_check('mm_hardware_idx_manufacturer') is None:
#         db_connection.db_query(
#             'CREATE INDEX mm_hardware_idx_manufacturer ON mm_hardware(mm_hardware_manufacturer)')
#     if db_connection.db_table_index_check('mm_hardware_idx_model') is None:
#         db_connection.db_query(
#             'CREATE INDEX mm_hardware_idx_model ON mm_hardware(mm_hardware_model)')
#     db_connection.db_version_update(20)
#     db_connection.db_commit()

# TODO add mm_metadata_album_image to mm_metadata_album

# TODO add mm_metadata_tvshow_user_json to mm_metadata_tvshow
# and index
# TODO add mm_metadata_music_user_json to mm_metadata_music
# and index
# TODO add mm_metadata_music_video_user_json to mm_metadata_music_video
# and index

# ("Comic", "Publication", True),
# ("Comic Strip", "Publication", True),
# db_connection.db_media_class_insert(
#            media_class[0], media_class[1], media_class[2])

'''
'LastFM': {'api_key': None,
           'api_secret': None,
           'username': None,
           'password': None},
'''

# if db_connection.db_version_check() < 22:
#     # game category
#     db_connection.db_query('create table IF NOT EXISTS mm_game_category (gc_id uuid'
#                            ' CONSTRAINT gc_id_pk primary key, gc_category text)')
#     if db_connection.db_table_index_check('gc_category_idx_name') is None:
#         db_connection.db_query('CREATE INDEX gc_category_idx_name'
#                                ' ON mm_game_category(gc_category)')
#     db_connection.db_version_update(22)
#     db_connection.db_commit()

#         "MetadataImageLocal": false to metadata json options


if db_connection.db_version_check() < 23:
    # retro update
    db_connection.db_cron_insert('Retro game data', 'Grab updated metadata for retro game(s)',
                                 False, 'Days 1', datetime.datetime(1970, 1, 1, 0, 0, 1),
                                 json.dumps({'exchange_key': 'mkque_ex', 'route_key': 'mkque',
                                             'Type': 'Cron Run',
                                             'program': '/mediakraken/subprogram_metadata_games.py'}),

                                 )
    db_connection.db_version_update(23)
    db_connection.db_commit()

# if db_connection.db_version_check() < 24:
#     options_json, status_json = db_connection.db_opt_status_read()
#     options_json['Docker Instances']['elk'] = False
#     db_connection.db_opt_update(json.dumps(options_json))
#     db_connection.db_version_update(24)
#     db_connection.db_commit()

if db_connection.db_version_check() < 25:
    options_json, status_json = db_connection.db_opt_status_read()
    db_connection.db_drop_table('mm_media_class')
    db_connection.db_query('ALTER TABLE mm_media DROP COLUMN mm_media_class_guid;')
    db_connection.db_query('ALTER TABLE mm_media ADD COLUMN mm_media_class_guid smallint;')
    db_connection.db_query('ALTER TABLE mm_media DROP COLUMN mm_media_class_guid;')
    db_connection.db_query('ALTER TABLE mm_media ADD COLUMN mm_media_class_guid smallint;')
    db_connection.db_query('ALTER TABLE mm_media_dir DROP COLUMN mm_media_dir_class_type;')
    db_connection.db_query(
        'ALTER TABLE mm_media_dir ADD COLUMN mm_media_dir_class_type smallint;')
    db_connection.db_query('ALTER TABLE mm_media_remote DROP COLUMN mmr_media_class_guid;')
    db_connection.db_query(
        'ALTER TABLE mm_media_remote ADD COLUMN mmr_media_class_guid smallint;')
    db_connection.db_version_update(25)
    db_connection.db_commit()

if db_connection.db_version_check() < 26:
    # game servers
    db_connection.db_query(
        'create table IF NOT EXISTS mm_game_dedicated_servers (mm_game_server_id uuid'
        ' CONSTRAINT mm_game_server_id primary key,'
        ' mm_game_server_name text,'
        ' mm_game_server_json jsonb)')
    db_connection.db_query(
        'CREATE INDEX mm_game_server_name_idx'
        ' ON mm_game_dedicated_servers(mm_game_server_name)')
    db_connection.db_version_update(26)
    db_connection.db_commit()

if db_connection.db_version_check() < 27:
    # user queue
    db_connection.db_query(
        'create table IF NOT EXISTS mm_user_queue (mm_user_queue_id uuid'
        ' CONSTRAINT mm_user_queue_id primary key,'
        ' mm_user_queue_name text,'
        ' mm_user_queue_user_id uuid,'
        ' mm_user_queue_media_type smallint)')
    db_connection.db_query('CREATE INDEX mm_user_queue_name_idx'
                           ' ON mm_user_queue(mm_user_queue_name)')
    db_connection.db_query('CREATE INDEX mm_user_queue_user_id_idx'
                           ' ON mm_user_queue(mm_user_queue_user_id)')
    db_connection.db_query('CREATE INDEX mm_user_queue_media_type_idx'
                           ' ON mm_user_queue(mm_user_queue_media_type)')
    db_connection.db_version_update(27)
    db_connection.db_commit()

if db_connection.db_version_check() < 28:
    options_json, status_json = db_connection.db_opt_status_read()
    db_connection.db_query(
        'ALTER TABLE mm_metadata_tvshow DROP COLUMN mm_metadata_media_tvshow_id;')
    db_connection.db_query(
        'ALTER TABLE mm_metadata_tvshow ADD COLUMN mm_metadata_media_tvshow_id integer;')
    db_connection.db_query('CREATE INDEX mm_metadata_media_tvshow_id_idx'
                           ' ON mm_metadata_tvshow(mm_metadata_media_tvshow_id)')
    db_connection.db_version_update(28)
    db_connection.db_commit()

if db_connection.db_version_check() < 29:
    options_json, status_json = db_connection.db_opt_status_read()
    options_json.update({'MAME': {'Version': 224}})
    db_connection.db_opt_update(json.dumps(options_json))
    db_connection.db_version_update(29)
    db_connection.db_commit()

if db_connection.db_version_check() < 30:
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN mdq_new_uuid uuid;')
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN mdq_class_uuid uuid;')
    db_connection.db_version_update(30)
    db_connection.db_commit()

if db_connection.db_version_check() < 31:
    try:
        db_connection.db_query('ALTER TABLE mm_review DROP COLUMN mm_review_metadata_id;')
    except:
        db_connection.db_rollback()
    db_connection.db_version_update(31)
    db_connection.db_commit()

if db_connection.db_version_check() < 32:
    try:
        db_connection.db_query('DROP TABLE mm_media_share;')
        db_connection.db_query('ALTER TABLE mm_media_dir DROP COLUMN mm_media_dir_share_guid;')
        db_connection.db_query('ALTER TABLE mm_media_dir ADD COLUMN mm_media_dir_username text;')
        db_connection.db_query('ALTER TABLE mm_media_dir ADD COLUMN mm_media_dir_password text;')
    except:
        db_connection.db_rollback()
    db_connection.db_version_update(32)
    db_connection.db_commit()

if db_connection.db_version_check() < 33:
    db_connection.db_query('ALTER TABLE mm_download_que DROP COLUMN mdq_class_uuid;')
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN mdq_class_uuid smallint;')
    db_connection.db_version_update(33)
    db_connection.db_commit()

if db_connection.db_version_check() < 34:
    db_connection.db_query('ALTER TABLE mm_link ADD COLUMN mm_link_username text;')
    db_connection.db_query('ALTER TABLE mm_link ADD COLUMN mm_link_password text;')
    db_connection.db_version_update(34)
    db_connection.db_commit()

if db_connection.db_version_check() < 35:
    db_connection.db_query(
        'create table IF NOT EXISTS mm_developer (mm_developer_id uuid'
        ' CONSTRAINT mm_developer_id primary key,'
        ' mm_developer_name text,'
        ' mm_developer_json jsonb)')
    db_connection.db_query('CREATE INDEX mm_developer_name_idx'
                           ' ON mm_developer(mm_developer_name)')
    db_connection.db_query(
        'create table IF NOT EXISTS mm_publisher (mm_publisher_id uuid'
        ' CONSTRAINT mm_publisher_id primary key,'
        ' mm_publisher_name text,'
        ' mm_publisher_json jsonb)')
    db_connection.db_query('CREATE INDEX mm_publisher_name_idx'
                           ' ON mm_publisher(mm_publisher_name)')
    db_connection.db_version_update(35)
    db_connection.db_commit()

if db_connection.db_version_check() < 36:
    options_json, status_json = db_connection.db_opt_status_read()
    options_json.update({'MAME': {'Version': 230}})
    db_connection.db_opt_update(json.dumps(options_json))
    db_connection.db_version_update(36)
    db_connection.db_commit()

if db_connection.db_version_check() < 37:
    db_connection.db_query('ALTER TABLE mm_metadata_game_software_info'
                           ' ADD COLUMN IF NOT EXISTS gi_game_info_sha1 text;')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_metadata_game_software_info_sha1_idx'
                           ' ON mm_metadata_game_software_info(gi_game_info_sha1)')
    db_connection.db_query('ALTER TABLE mm_metadata_game_software_info'
                           ' ADD COLUMN IF NOT EXISTS gi_game_info_blake3 text;')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_metadata_game_software_info_blake3_idx'
                           ' ON mm_metadata_game_software_info(gi_game_info_blake3)')
    db_connection.db_version_update(37)
    db_connection.db_commit()

if db_connection.db_version_check() < 38:
    db_connection.db_query('ALTER TABLE mm_download_que DROP COLUMN if exists mdq_class_uuid;')
    db_connection.db_version_update(38)
    db_connection.db_commit()

if db_connection.db_version_check() < 39:
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_metadata_movie_ndx_media_id'
                           ' ON mm_metadata_movie(mm_metadata_media_id)')
    db_connection.db_query('DROP INDEX if exists mm_metadata_idxgin_media_id')
    db_connection.db_version_update(39)
    db_connection.db_commit()

if db_connection.db_version_check() < 40:
    # mm_loan
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_loan_ndx_media_id'
                           ' ON mm_loan(mm_loan_media_id)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_loan_ndx_user_id'
                           ' ON mm_loan(mm_loan_user_id)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_loan_ndx_user_loan_id'
                           ' ON mm_loan(mm_load_user_loan_id)')
    # mm_media_remote
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_media_remote_ndx_link_id'
                           ' ON mm_media_remote(mmr_media_link_id)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_media_remote_ndx_media_id'
                           ' ON mm_media_remote(mmr_media_uuid)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_media_remote_ndx_meta_id'
                           ' ON mm_media_remote(mmr_media_metadata_guid)')
    # mm_metadata_anime
    db_connection.db_query('ALTER TABLE mm_metadata_anime'
                           ' RENAME COLUMN mm_media_anime_name TO mm_metadata_anime_name;')
    db_connection.db_query('ALTER TABLE mm_metadata_anime'
                           ' DROP COLUMN mm_metadata_anime_media_id')
    db_connection.db_query('ALTER TABLE mm_metadata_anime'
                           ' ADD COLUMN mm_metadata_anime_media_id integer;')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_metadata_anime_ndx_media_id'
                           ' ON mm_metadata_anime(mm_metadata_anime_media_id)')
    db_connection.db_query('DROP INDEX if exists mm_metadata_anime_idxgin_media_id_anidb')
    db_connection.db_query('DROP INDEX if exists mm_metadata_anime_idxgin_media_id_imdb')
    db_connection.db_query('DROP INDEX if exists mm_metadata_anime_idxgin_media_id_thetvdb')
    db_connection.db_query('DROP INDEX if exists mm_metadata_anime_idxgin_media_id_tmdb')
    # mm_metadata_game_systems_info
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_metadata_game_systems_info_ndx_name'
                           ' ON mm_metadata_game_systems_info(gs_game_system_name)')
    # mm_metadata_movie
    db_connection.db_query('ALTER TABLE mm_metadata_movie'
                           ' RENAME COLUMN mm_media_name TO mm_metadata_name;')
    # mm_notification
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_notification_ndx_time'
                           ' ON mm_notification(mm_notification_time)')
    # mm_radio
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_radio_ndx_name'
                           ' ON mm_radio(mm_radio_name)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_radio_ndx_active'
                           ' ON mm_radio(mm_radio_active)')
    # mm_tv_schedule
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_tv_schedule_ndx_station_id'
                           ' ON mm_tv_schedule(mm_tv_schedule_station_id)')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_tv_schedule_ndx_schedule_date'
                           ' ON mm_tv_schedule(mm_tv_schedule_date)')
    db_connection.db_version_update(40)
    db_connection.db_commit()

if db_connection.db_version_check() < 41:
    # mm_download_que
    db_connection.db_query('LOCK mm_download_que in ACCESS EXCLUSIVE mode')
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN'
                           ' IF NOT EXISTS mdq_provider_id integer;')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_download_que_ndx_provider_id'
                           ' ON mm_download_que(mdq_provider_id)')
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN'
                           ' IF NOT EXISTS mdq_status text;')
    db_connection.db_query('CREATE INDEX IF NOT EXISTS mm_download_que_ndx_status'
                           ' ON mm_download_que(mdq_status)')
    db_connection.db_query('ALTER TABLE mm_download_que ADD COLUMN'
                           ' IF NOT EXISTS mdq_path text;')
    for row_data in db_connection.db_query('select mdq_id, mdq_download_json from mm_download_que'):
        if 'Path' in row_data['mdq_download_json']:
            path_data = str(row_data['mdq_download_json']['Path'])
        else:
            path_data = 'NULL'
        sql_command = 'update mm_download_que set mdq_provider_id=' \
                      + str(row_data['mdq_download_json']['ProviderMetaID']) \
                      + ', mdq_status=\"' + row_data['mdq_download_json']['Status'] \
                      + '\", mdq_path=' + path_data \
                      + ' where mdq_id=' + str(row_data['mdq_id']) + ')'
        db_connection.db_query(sql_command)
    db_connection.db_query('ALTER TABLE mm_download_que DROP COLUMN'
                           ' IF EXISTS mdq_download_json;')
    db_connection.db_version_update(41)
    db_connection.db_commit()

'''
    # mm_metadata_music_video
    # TODO
    # mm_metadata_musician
    # TODO
    # mm_metadata_sports
    # TODO
    # mm_tv_schedule_program
    # TODO
    # mm_tv_stations
    # TODO
    # mm_user
    # TODO
    # mm_user_activity
    # TODO
    # mm_user_group
    # TODO
    # mm_user_profile
    # TODO
    # mm_user_queue
    # TODO    
'''

# TODO add the rename to cron program names
# TODO add the rename to cron program names
# TODO add the rename to cron program names
# TODO add the rename to cron program names

# close the database
db_connection.db_close()

if dont_force_localhost:
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='STOP')
