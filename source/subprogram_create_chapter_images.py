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

import json
import os
import subprocess
import uuid

from concurrent.futures import ThreadPoolExecutor

from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_metadata

# set before everything else
total_images_created = 0


def worker(worker_file_list):
    global total_images_created
    chapter_image_list = {}
    json_id, json_data, json_obj, media_path = worker_file_list
    # open the database
    option_config_json, thread_db = common_config_ini.com_config_read()
    # begin image generation
    chapter_count = 0
    first_image = True
    for chapter_data in json_obj['chapters']:
        chapter_count += 1
        # file path, time, output name
        # check image save option whether to save this in media folder or metadata folder
        if option_config_json['MetadataImageLocal'] == False:
            image_file_path = os.path.join(common_metadata.com_meta_image_file_path(media_path,
                                                                                    'chapter'),
                                           (str(uuid.uuid4()) + '.png'))
        else:
            image_file_path = os.path.join(os.path.dirname(media_path),
                                           'chapters')
            # have this bool so I don't hit the os looking for path each time
            if first_image == True and not os.path.isdir(image_file_path):
                os.makedirs(image_file_path)
            image_file_path = os.path.join(
                image_file_path, (str(chapter_count) + '.png'))
        command_list = []
        command_list.append('./bin/ffmpeg')
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
        command_list.append(image_file_path)
        ffmpeg_proc = subprocess.Popen(command_list, shell=False)
        ffmpeg_proc.wait()  # wait for subprocess to finish to not flood with ffmpeg processes
        # as the worker might see it as finished if allowed to continue
        chapter_image_list[chapter_data['tags']['title']] = image_file_path
        total_images_created += 1
        first_image = False
    if json_data is None:
        json_data = json.dumps(
            {'ChapterScan': False, 'ChapterImages': chapter_image_list})
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
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_create_chapter_images')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# begin the media match on NULL matches
file_list = []
for row_data in db_connection.db_known_media_chapter_scan():
    # from query 0-mm_media_guid, 1-mm_media_json, 2-mm_media_ffprobe_json, 3-mm_media_path
    # loop through ffprobe json chapter data
    if row_data['mm_media_ffprobe_json'] is not None:
        file_list.append(row_data)

# start processing the files
if len(file_list) > 0:
    with ThreadPoolExecutor(len(file_list)) as executor:
        futures = [executor.submit(worker, n) for n in file_list]
        for future in futures:
            common_global.es_inst.es_index('info', {'data': future.result()})

# send notications
if total_images_created > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(
            total_images_created)
        + " chapter image(s) generated.", True)

# commit all changes
db_connection.db_commit()

# close the database
db_connection.db_close()
