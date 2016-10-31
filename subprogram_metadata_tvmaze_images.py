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
import os
import uuid
import json
from common import common_config_ini
from common import common_logging
from common import common_metadata
from common import common_network
from common import common_signal
import locale
locale.setlocale(locale.LC_ALL, '')


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_tvmaze_Images')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server tvmaze Images Start', None,\
    'System: Server tvmaze Images Start', 'ServertvmazeImagesStart', None, None, 'System')


# prep totals
total_cast_images = 0
total_char_images = 0
total_episode_images = 0


# grab tvmaze ones without image data
for row_data in db_connection.db_meta_tvshow_images_to_update('tvmaze'):
    logging.info("json: %s", row_data['mm_metadata_tvshow_json'])
    # this is "removed" via the query ['Meta']['tvmaze']
    # grab poster
    poster_image_local = None
    if 'image' in row_data['mm_metadata_tvshow_json']\
            and row_data['mm_metadata_tvshow_json']['image'] is not None:
        if 'original' in row_data['mm_metadata_tvshow_json']['image']:
            poster_image_local = os.path.join(common_metadata.com_meta_image_file_path(\
                row_data['mm_metadata_tvshow_json']['name'], 'poster'), (str(uuid.uuid4())\
                + '.' + row_data['mm_metadata_tvshow_json']['image']['original'].rsplit('.', 1)[1]))
            common_network.mk_network_fetch_from_url(\
                row_data['mm_metadata_tvshow_json']['image']['original'], poster_image_local)
    # generate image json
    json_image_data = {'Images': {'tvmaze': {'Banner': None, 'Fanart': None,\
        'Poster': poster_image_local, 'Cast': {}, 'Characters': {}, 'Episodes': {}, "Redo": False}}}
    # process person and character data
    for cast_member in row_data['mm_metadata_tvshow_json']['_embedded']['cast']:
        if cast_member['person']['image'] is not None\
                and 'original' in cast_member['person']['image']:
            # determine path and fetch image/save
            cast_image_local = os.path.join(common_metadata.com_meta_image_file_path(\
                cast_member['person']['name'], 'person'), (str(uuid.uuid4()) + '.'\
                + cast_member['person']['image']['original'].rsplit('.', 1)[1]))
            logging.info("one: %s", cast_image_local)
            common_network.mk_network_fetch_from_url(cast_member['person']['image']['original'],\
                cast_image_local)
            json_image_data['Images']['tvmaze']['Cast'][cast_member['person']['id']]\
                = cast_image_local
            total_cast_images += 1
        if 'image' in cast_member['character']:
            if cast_member['character']['image'] is not None:
                if 'original' in cast_member['character']['image']:
                    char_image_local = os.path.join(common_metadata.com_meta_image_file_path(\
                        cast_member['character']['name'], 'character'), (str(uuid.uuid4()) + '.'\
                        + cast_member['character']['image']['original'].rsplit('.', 1)[1]))
                    logging.info("two: %s", char_image_local)
                    common_network.mk_network_fetch_from_url(\
                        cast_member['character']['image']['original'], char_image_local)
                    json_image_data['Images']['tvmaze']['Characters']\
                        [cast_member['character']['id']] = char_image_local
                    total_char_images += 1
    # process episode data
    for episode_info in row_data['mm_metadata_tvshow_json']['_embedded']['episodes']:
        if episode_info['image'] is not None:
            if 'original' in episode_info['image']:
                eps_image_local = os.path.join(common_metadata.com_meta_image_file_path(\
                    episode_info['name'], 'backdrop'), (str(uuid.uuid4()) + '.'\
                    + episode_info['image']['original'].rsplit('.', 1)[1]))
                logging.info("eps: %s", eps_image_local)
                common_network.mk_network_fetch_from_url(episode_info['image']['original'],\
                    eps_image_local)
                json_image_data['Images']['tvmaze']['Episodes'][episode_info['id']]\
                    = eps_image_local
                total_episode_images += 1
    db_connection.db_meta_tvshow_update_image(json.dumps(json_image_data), row_data[1])
    # commit
    db_connection.db_commit()


# send notifications
if total_cast_images > 0:
    db_connection.db_notification_insert(locale.format('%d', total_cast_images, True)\
        + " new TV cast image(s) added.", True)
if total_char_images > 0:
    db_connection.db_notification_insert(locale.format('%d', total_char_images, True)\
        + " new TV character image(s) added.", True)
if total_episode_images > 0:
    db_connection.db_notification_insert(locale.format('%d', total_episode_images, True)\
        + " new TV episode image(s) added.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server tvmaze Images Stop', None,\
    'System: Server tvmaze Images Stop', 'ServertvmazeImagesStop', None, None, 'System')


# commit all changes
db_connection.db_commit()


# close the database
db_connection.db_close()
