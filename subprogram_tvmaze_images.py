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
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import os
import uuid
import signal
import json
import sys
sys.path.append("../MediaKraken_Server")
sys.path.append("../MediaKraken_Common")
import common_file
import common_logging
import common_Metadata
import common_network
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')


# create the file for pid
pid_file = '../pid/' + str(os.getpid())
common_file.common_file_Save_Data(pid_file, 'TVMaze_Images_Known', False, False, None)


def signal_receive(signum, frame):
    print('CHILD TVMaze Images: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db.MK_Server_Database_Rollback()
    db.MK_Server_Database_Close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.common_logging_Start('./log/MediaKraken_Subprogram_TVMaze_Images')


# open the database
db = database_base.MK_Server_Database()
db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(),\
    Config.get('DB Connections', 'PostDBPort').strip(),\
    Config.get('DB Connections', 'PostDBName').strip(),\
    Config.get('DB Connections', 'PostDBUser').strip(),\
    Config.get('DB Connections', 'PostDBPass').strip())


# log start
db.MK_Server_Database_Activity_Insert('MediaKraken_Server TVMaze Images Start', None,\
    'System: Server TVMaze Images Start', 'ServerTVMazeImagesStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# prep totals
total_cast_images = 0
total_char_images = 0
total_episode_images = 0


# grab tvmaze ones without image data
for row_data in db.MK_Server_Database_Metadata_TVShow_Images_To_Update('TVMaze'):
    logging.debug("json: %s", row_data['mm_metadata_tvshow_json'])
    # this is "removed" via the query ['Meta']['TVMaze']
    # grab poster
    poster_image_local = None
    if 'image' in row_data['mm_metadata_tvshow_json'] and row_data['mm_metadata_tvshow_json']['image'] is not None:
        if 'original' in row_data['mm_metadata_tvshow_json']['image']:
            poster_image_local = os.path.join(com_Metadata.com_Metadata_Image_File_Path(row_data['mm_metadata_tvshow_json']['name'], 'poster'), (str(uuid.uuid4()) + '.' + row_data['mm_metadata_tvshow_json']['image']['original'].rsplit('.', 1)[1]))
            common_network.MK_Network_Fetch_From_URL(row_data['mm_metadata_tvshow_json']['image']['original'], poster_image_local)
    # generate image json
    json_image_data = {'Images': {'TVMaze': {'Banner': None, 'Fanart': None, 'Poster': poster_image_local, 'Cast': {}, 'Characters': {}, 'Episodes': {}, "Redo": False}}}
    # process person and character data
    for cast_member in row_data['mm_metadata_tvshow_json']['_embedded']['cast']:
        if cast_member['person']['image'] is not None and 'original' in cast_member['person']['image']:
            # determine path and fetch image/save
            cast_image_local = os.path.join(com_Metadata.com_Metadata_Image_File_Path(cast_member['person']['name'], 'person'), (str(uuid.uuid4()) + '.' + cast_member['person']['image']['original'].rsplit('.', 1)[1]))
            logging.debug("one: %s", cast_image_local)
            common_network.MK_Network_Fetch_From_URL(cast_member['person']['image']['original'], cast_image_local)
            json_image_data['Images']['TVMaze']['Cast'][cast_member['person']['id']] = cast_image_local
            total_cast_images += 1
        if 'image' in cast_member['character']:
            if cast_member['character']['image'] is not None:
                if 'original' in cast_member['character']['image']:
                    char_image_local = os.path.join(com_Metadata.com_Metadata_Image_File_Path(cast_member['character']['name'], 'character'), (str(uuid.uuid4()) + '.' + cast_member['character']['image']['original'].rsplit('.', 1)[1]))
                    logging.debug("two: %s", char_image_local)
                    common_network.MK_Network_Fetch_From_URL(cast_member['character']['image']['original'], char_image_local)
                    json_image_data['Images']['TVMaze']['Characters'][cast_member['character']['id']] = char_image_local
                    total_char_images += 1
    # process episode data
    for episode_info in row_data['mm_metadata_tvshow_json']['_embedded']['episodes']:
        if episode_info['image'] is not None:
            if 'original' in episode_info['image']:
                eps_image_local = os.path.join(com_Metadata.com_Metadata_Image_File_Path(episode_info['name'], 'backdrop'), (str(uuid.uuid4()) + '.' + episode_info['image']['original'].rsplit('.', 1)[1]))
                logging.debug("eps: %s", eps_image_local)
                common_network.MK_Network_Fetch_From_URL(episode_info['image']['original'], eps_image_local)
                json_image_data['Images']['TVMaze']['Episodes'][episode_info['id']] = eps_image_local
                total_episode_images += 1
    db.MK_Server_Database_Metadata_TVShow_Update_Image(json.dumps(json_image_data), row_data[1])
    # commit
    db.MK_Server_Database_Commit()


# send notifications
if total_cast_images > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', total_cast_images, True)\
        + " new TV cast image(s) added.", True)
if total_char_images > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', total_char_images, True)\
        + " new TV character image(s) added.", True)
if total_episode_images > 0:
    db.MK_Server_Database_Notification_Insert(locale.format('%d', total_episode_images, True)\
        + " new TV episode image(s) added.", True)

# log end
db.MK_Server_Database_Activity_Insert('MediaKraken_Server TVMaze Images Stop', None,\
    'System: Server TVMaze Images Stop', 'ServerTVMazeImagesStop', None, None, 'System')

# commit all changes
db.MK_Server_Database_Commit()

# close the database
db.MK_Server_Database_Close()
