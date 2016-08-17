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
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import os
import uuid
import signal
import json
import sys
sys.path.append("./server")
sys.path.append("./common")
from common import common_file
from common import common_logging
from common import common_metadata
from common import common_network
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'TVDB_Images_Known', False, False, None)


def signal_receive(signum, frame):
    print('CHILD thetvdb Images: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.srv_db_rollback()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_thetvdb_Images')


# open the database
db = database_base.MKServerDatabase()
db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
    config_handle.get('DB Connections', 'PostDBPort').strip(),\
    config_handle.get('DB Connections', 'PostDBName').strip(),\
    config_handle.get('DB Connections', 'PostDBUser').strip(),\
    config_handle.get('DB Connections', 'PostDBPass').strip())


# log start
db.srv_db_activity_insert('MediaKraken_Server thetvdb Images Start', None,\
    'System: Server tvmaze Images Start', 'ServerTVDBImagesStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# prep totals
total_cast_images = 0
total_episode_images = 0


# grab ones without image data
for row_data in db.srv_db_meta_tvshow_images_to_update('thetvdb'):
    logging.debug("json: %s", row_data['mm_metadata_tvshow_json']['Meta']['Series'])
    # this is "removed" via the query ['Meta']['thetvdb']

    # grab poster
    poster_image_local = None
    if 'poster' in row_data['mm_metadata_tvshow_json']['Meta']['Series']\
            and row_data['mm_metadata_tvshow_json']['Meta']['Series']['poster'] is not None:
        poster_image_local = os.path.join(com_metadata.com_meta_image_file_path(row_data['mm_metadata_tvshow_json']['Meta']['Series']['SeriesName'], 'poster'), (str(uuid.uuid4()) + '.' + row_data['mm_metadata_tvshow_json']['Meta']['Series']['poster'].rsplit('.', 1)[1]))
        common_network.mk_network_fetch_from_url("https://thetvdb.com/banners/" + row_data['mm_metadata_tvshow_json']['Meta']['Series']['poster'], poster_image_local)

    # grab banner
    banner_image_local = None
    if 'banner' in row_data['mm_metadata_tvshow_json']['Meta']['Series']\
            and row_data['mm_metadata_tvshow_json']['Meta']['Series']['banner'] is not None:
        banner_image_local = os.path.join(com_metadata.com_meta_image_file_path(row_data['mm_metadata_tvshow_json']['Meta']['Series']['SeriesName'], 'banner'), (str(uuid.uuid4()) + '.' + row_data['mm_metadata_tvshow_json']['Meta']['Series']['banner'].rsplit('.', 1)[1]))
        common_network.mk_network_fetch_from_url("https://thetvdb.com/banners/" + row_data['mm_metadata_tvshow_json']['Meta']['Series']['banner'], banner_image_local)

    # grab fanart
    fanart_image_local = None
    if 'fanart' in row_data['mm_metadata_tvshow_json']['Meta']['Series']\
            and row_data['mm_metadata_tvshow_json']['Meta']['Series']['fanart'] is not None:
        fanart_image_local = os.path.join(com_metadata.com_meta_image_file_path(row_data['mm_metadata_tvshow_json']['Meta']['Series']['SeriesName'], 'fanart'), (str(uuid.uuid4()) + '.' + row_data['mm_metadata_tvshow_json']['Meta']['Series']['fanart'].rsplit('.', 1)[1]))
        common_network.mk_network_fetch_from_url("https://thetvdb.com/banners/" + row_data['mm_metadata_tvshow_json']['Meta']['Series']['fanart'], fanart_image_local)

    # generate image json
    json_image_data = {'Images': {'thetvdb': {'Banner': banner_image_local, 'Fanart': fanart_image_local, 'Poster': poster_image_local, 'Cast': {}, 'Characters': {}, 'Episodes': {}, "Redo": False}}}
    logging.debug("image: %s", json_image_data)

    # process person and character data
    if 'Cast' in row_data['mm_metadata_tvshow_json']\
            and row_data['mm_metadata_tvshow_json']['Cast'] is not None:
        logging.debug("huh?: %s", row_data['mm_metadata_tvshow_json']['Cast'])
        if 'Actor' in row_data['mm_metadata_tvshow_json']['Cast']:
            for cast_member in row_data['mm_metadata_tvshow_json']['Cast']['Actor']:
                logging.debug("wha: %s", cast_member)
                if cast_member['Image'] is not None:
                    # determine path and fetch image/save
                    cast_image_local = os.path.join(com_metadata.com_meta_image_file_path(cast_member['Name'],\
                        'person'), (str(uuid.uuid4()) + '.' + cast_member['Image'].rsplit('.', 1)[1]))
                    logging.debug("one: %s", cast_image_local)
                    common_network.mk_network_fetch_from_url("https://thetvdb.com/banners/" + cast_member['Image'], cast_image_local)
                    json_image_data['Images']['thetvdb']['Cast'][cast_member['id']] = cast_image_local
                    total_cast_images += 1
            logging.debug("cast: %s", json_image_data)

    # process episode data
    if 'Episode' in row_data['mm_metadata_tvshow_json']['Meta']:
        for episode_info in row_data['mm_metadata_tvshow_json']['Meta']['Episode']:
            logging.debug("episode: %s", episode_info)
            if episode_info['filename'] is not None:
                eps_image_local = os.path.join(com_metadata.com_meta_image_file_path(episode_info['EpisodeName'],\
                'backdrop'), (str(uuid.uuid4()) + '.' + episode_info['filename'].rsplit('.', 1)[1]))
                logging.debug("eps: %s", eps_image_local)
                common_network.mk_network_fetch_from_url("https://thetvdb.com/banners/"\
                    + episode_info['filename'], eps_image_local)
                json_image_data['Images']['thetvdb']['Episodes'][episode_info['id']] = eps_image_local
                total_episode_images += 1
    db.srv_db_meta_tvshow_update_image(json.dumps(json_image_data), row_data[1])
    # commit
    db.srv_db_commit()


# send notifications
if total_cast_images > 0:
    db.srv_db_notification_insert(locale.format('%d', total_cast_images, True)\
        + " new TV cast image(s) added.", True)
if total_episode_images > 0:
    db.srv_db_notification_insert(locale.format('%d', total_episode_images, True)\
        + " new TV episode image(s) added.", True)

# log end
db.srv_db_activity_insert('MediaKraken_Server thetvdb Images Stop', None,\
    'System: Server thetvdb Images Stop', 'ServerTVDBImagesStop', None, None, 'System')

# commit all changes
db.srv_db_commit()

# close the database
db.srv_db_close()
