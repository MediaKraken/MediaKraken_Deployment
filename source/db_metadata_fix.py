"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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
import os

from common import common_config_ini
from common import common_logging_elasticsearch_httpx

dont_force_localhost = True

if dont_force_localhost:
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='START',
                                                         index_name='db_metadata_fix')
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read()
else:
    # open the database
    option_config_json, db_connection = common_config_ini.com_config_read(force_local=True)

total_movie = 0
total_tv = 0
total_person = 0
# read in all mm_metadata_movie where mm_metadata_localimage_json is not null
for metadata_record in db_connection.db_query('select mm_metadata_media_id,'
                                              ' mm_metadata_localimage_json'
                                              ' from mm_metadata_movie'
                                              ' where mm_metadata_localimage_json'
                                              ' is not null'):
    new_json = metadata_record['mm_metadata_localimage_json']
    if metadata_record['mm_metadata_localimage_json']['Poster'] is not None:
        if not os.path.exists('/mediakraken/web_app_sanic/static' +
                              metadata_record['mm_metadata_localimage_json']['Poster']):
            new_json['Poster'] = None
            db_connection.db_query('update mm_metadata_movie'
                                   ' set mm_metadata_localimage_json=\''
                                   + json.dumps(new_json)
                                   + '\' where mm_metadata_media_id = \''
                                   + str(metadata_record['mm_metadata_media_id']) + '\'')
            print('Movie Poster BAD: ', metadata_record['mm_metadata_media_id'], flush=True)
            total_movie += 1
    if metadata_record['mm_metadata_localimage_json']['Backdrop'] is not None:
        if not os.path.exists('/mediakraken/web_app_sanic/static' +
                              metadata_record['mm_metadata_localimage_json']['Backdrop']):
            new_json['Backdrop'] = None
            db_connection.db_query('update mm_metadata_movie'
                                   ' set mm_metadata_localimage_json=\''
                                   + json.dumps(new_json)
                                   + '\' where mm_metadata_media_id = \''
                                   + str(metadata_record['mm_metadata_media_id']) + '\'')
            print('Movie Backdrop BAD: ', metadata_record['mm_metadata_media_id'], flush=True)
            total_movie += 1

for metadata_record in db_connection.db_query('select mm_metadata_media_tvshow_id,'
                                              ' mm_metadata_tvshow_localimage_json'
                                              ' from mm_metadata_tvshow'
                                              ' where mm_metadata_tvshow_localimage_json'
                                              ' is not null'):
    new_json = metadata_record['mm_metadata_tvshow_localimage_json']
    if metadata_record['mm_metadata_tvshow_localimage_json']['Poster'] is not None:
        if not os.path.exists('/mediakraken/web_app_sanic/static' +
                              metadata_record['mm_metadata_tvshow_localimage_json']['Poster']):
            new_json['Poster'] = None
            db_connection.db_query('update mm_metadata_tvshow'
                                   ' set mm_metadata_tvshow_localimage_json=\''
                                   + json.dumps(new_json)
                                   + '\' where mm_metadata_media_tvshow_id = \''
                                   + str(metadata_record['mm_metadata_media_tvshow_id']) + '\'')

            print('TV Poster BAD: ', metadata_record['mm_metadata_media_tvshow_id'], flush=True)
            total_tv += 1
    if metadata_record['mm_metadata_tvshow_localimage_json']['Backdrop'] is not None:
        if not os.path.exists('/mediakraken/web_app_sanic/static' +
                              metadata_record['mm_metadata_tvshow_localimage_json']['Backdrop']):
            new_json['Backdrop'] = None
            db_connection.db_query('update mm_metadata_tvshow'
                                   ' set mm_metadata_tvshow_localimage_json=\''
                                   + json.dumps(new_json)
                                   + '\' where mm_metadata_media_tvshow_id = \''
                                   + str(metadata_record['mm_metadata_media_tvshow_id']) + '\'')

            print('TV Backdrop BAD: ', metadata_record['mm_metadata_media_tvshow_id'], flush=True)
            total_tv += 1

for metadata_record in db_connection.db_query('select mmp_id,'
                                              ' mmp_person_image,'
                                              ' mmp_person_meta_json->\'profile_path\' as profile'
                                              ' from mm_metadata_person'
                                              ' where mmp_person_image'
                                              ' is not null'):
    if metadata_record['profile'] is None \
            or not os.path.exists('/mediakraken/web_app_sanic/static' +
                                  metadata_record['mmp_person_image']
                                  + metadata_record['profile']):
        db_connection.db_query('update mm_metadata_person set mmp_person_image=Null'
                               ' where mmp_id = \'' + str(metadata_record['mmp_id']) + '\'')
        print('Person Poster BAD: ', str(metadata_record['mmp_id']), flush=True)
        total_person += 1

db_connection.db_commit()

# close the database
db_connection.db_close()

print('Movie: ', total_movie, flush=True)
print('TV: ', total_tv, flush=True)
print('Person: ', total_person, flush=True)

if dont_force_localhost:
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='STOP')
