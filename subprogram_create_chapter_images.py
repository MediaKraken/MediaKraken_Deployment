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
import logging # pylint: disable=W0611
import sys
import json
import uuid
import signal
import subprocess
import os
from common import common_config_ini
from common import common_file
from common import common_logging
from common import common_metadata
#from common import common_system
from concurrent import futures
import database as database_base
import locale
locale.setlocale(locale.LC_ALL, '')

# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Chapter_Images', False, False, None)

# set before everything else
total_images_created = 0


def signal_receive(signum, frame):
    print('CHILD Chapter Image: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    db_connection.db_rollback()
    db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)


def worker(worker_file_list):
    global total_images_created
    chapter_image_list = {}
    json_id, json_data, json_obj, media_path = worker_file_list
    #logging.debug('value=%s', json_id)
    thread_db = database_base.MKServerDatabase()
    thread_db.db_open(config_handle['DB Connections']['PostDBHost'],\
        config_handle['DB Connections']['PostDBPort'],\
        config_handle['DB Connections']['PostDBName'],\
        config_handle['DB Connections']['PostDBUser'],\
        config_handle['DB Connections']['PostDBPass'])
    # begin image generation
    for chapter_data in json_obj['chapters']:
        # file path, time, output name
        file_path = os.path.join(common_metadata.com_meta_image_file_path(media_path,\
            'chapter'), (str(uuid.uuid4()) + '.png'))
        command_list = []
        command_list.append('ffmpeg')
        # if ss is before the input it seeks and doesn't convert every frame like after input
        command_list.append('-ss')
        # format the seconds to what ffmpeg is looking for
        minutes, seconds = divmod(float(chapter_data['start_time']), 60)
        hours, minutes = divmod(minutes, 60)
        command_list.append("%02d:%02d:%02f" % (hours, minutes, seconds))
        command_list.append('-i')
        command_list.append(media_path)
        command_list.append('-vframes')
        command_list.append('1')
        command_list.append(file_path)
        ffmpeg_proc = subprocess.Popen(command_list, shell=False)
        ffmpeg_proc.wait() # wait for subprocess to finish to not flood with ffmpeg processes
        # as the worker might see it as finished if allowed to continue
        chapter_image_list[chapter_data['tags']['title']] = file_path
        total_images_created += 1
    if json_data is None:
        json_data = json.dumps({'ChapterScan':False, 'ChapterImages':chapter_image_list})
    else:
        json_data['ChapterScan'] = False
        json_data['ChapterImages'] = chapter_image_list
    # update the media row with the fact chapters images were created
    # and their filenames for the chapter images that were created
    thread_db.db_update_media_json(json_id, json.dumps(json_data))
    # commit after each one to not cause dupe images I guess?
    thread_db.db_commit()
    thread_db.db_close()
    return


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Create_Chapter_Images')


# open the database
config_handle, option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Create Chapter Start', None,\
    'System: Server Create Chapter Start', 'ServerCreateChapterStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# begin the media match on NULL matches
file_list = []
for row_data in db_connection.db_known_media_chapter_scan():
    # from query 0-mm_media_guid, 1-mm_media_json, 2-mm_media_ffprobe_json, 3-mm_media_path
    # loop through ffprobe json chapter data
    if row_data['mm_media_ffprobe_json'] is not None:
        file_list.append(row_data)


# start processing the files
if len(file_list) > 0:
    with futures.ThreadPoolExecutor(len(file_list)) as executor:
        futures = [executor.submit(worker, n) for n in file_list]
        for future in futures:
            logging.debug(future.result())


# send notications
if total_images_created > 0:
    db_connection.db_notification_insert(locale.format('%d', total_images_created, True)\
        + " chapter image(s) generated.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Create Chapter Stop', None,\
    'System: Server Create Chapter Stop', 'ServerCreateChapterStop', None, None, 'System')


# commit all changes
db_connection.db_commit()


# close the database
db_connection.db_close()


# remove pid
os.remove(pid_file)
