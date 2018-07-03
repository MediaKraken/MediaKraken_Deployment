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
import time
import uuid
from datetime import datetime  # to handle threading

import pika
from common import common_config_ini
from common import common_file
from common import common_file_extentions
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_network_cifs
from common import common_string

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_file_scan')


def worker(audit_directory):
    """
    Worker thread for each directory
    """
    dir_path, media_class_type_uuid, dir_guid = audit_directory
    # open the database
    option_config_json, thread_db = common_config_ini.com_config_read()
    common_global.es_inst.com_elastic_index('info', {'worker dir': dir_path})
    # update the timestamp now so any other media added DURING this scan don't get skipped
    thread_db.db_audit_dir_timestamp_update(dir_path)
    thread_db.db_audit_path_update_status(dir_guid,
                                          json.dumps({'Status': 'File search scan', 'Pct': 0}))
    thread_db.db_commit()
    # check for UNC before grabbing dir list
    if dir_path[:1] == "\\":
        file_data = []
        smb_stuff = common_network_cifs.CommonCIFSShare()
        addr, share, path = common_string.com_string_unc_to_addr_path(dir_path)
        smb_stuff.com_cifs_connect(addr)
        for dir_data in smb_stuff.com_cifs_walk(share, path):
            for file_name in dir_data[2]:
                file_data.append('\\\\' + addr + '\\' + share + '\\' + dir_data[0]
                                 + '\\' + file_name)
        smb_stuff.com_cifs_close()
    else:
        file_data = common_file.com_file_dir_list(dir_path, None, True, False)
    total_file_in_dir = len(file_data)
    total_scanned = 0
    total_files = 0
    for file_name in file_data:
        if file_name in global_known_media:
            pass
        else:
            filename_base, file_extension = os.path.splitext(file_name)
            if file_extension[1:].lower() in common_file_extentions.MEDIA_EXTENSION \
                    or file_extension[1:].lower() in common_file_extentions.SUBTITLE_EXTENSION:
                save_dl_record = True
                # check for "stacked" media file
                head, base_file_name = os.path.split(file_name)
                if common_string.STACK_CD.search(base_file_name) is not None \
                        or common_string.STACK_PART.search(base_file_name) is not None \
                        or common_string.STACK_DVD.search(base_file_name) is not None \
                        or common_string.STACK_PT.search(base_file_name) is not None \
                        or common_string.STACK_DISK.search(base_file_name) is not None \
                        or common_string.STACK_DISC.search(base_file_name) is not None:
                    # check to see if it's part one or not
                    if common_string.STACK_CD1.search(base_file_name) is None \
                            and common_string.STACK_PART1.search(base_file_name) is None \
                            and common_string.STACK_DVD1.search(base_file_name) is None \
                            and common_string.STACK_PT1.search(base_file_name) is None \
                            and common_string.STACK_DISK1.search(base_file_name) is None \
                            and common_string.STACK_DISC1.search(base_file_name) is None:
                        # it's not a part one here so, no DL record needed
                        save_dl_record = False
                total_files += 1
                filename_base, file_extension = os.path.splitext(file_name)
                new_class_type_uuid = media_class_type_uuid
                # video game data, don't do ffmpeg
                if thread_db.db_media_class_by_uuid(media_class_type_uuid) == 'Video Game':
                    if file_extension.lower() == 'iso':
                        new_class_type_uuid = class_text_dict['Game ISO']
                    elif file_extension.lower() == 'chd':
                        new_class_type_uuid = class_text_dict['Game CHD']
                    else:
                        new_class_type_uuid = class_text_dict['Game ROM']
                    # TODO lookup game info in game database data
                    media_ffprobe_json = None
                # if an extention skip
                elif file_extension.lower() in common_file_extentions.MEDIA_EXTENSION_SKIP_FFMPEG \
                        or file_extension.lower() in common_file_extentions.SUBTITLE_EXTENSION:
                    media_ffprobe_json = None
                    if file_extension.lower() in common_file_extentions.SUBTITLE_EXTENSION:
                        new_class_type_uuid = class_text_dict['Subtitle']
                else:
                    if file_name.find('/trailers/') != -1 \
                            or file_name.find('\\trailers\\') != -1 \
                            or file_name.find('/theme.mp3') != -1 \
                            or file_name.find('\\theme.mp3') != -1 \
                            or file_name.find('/theme.mp4') != -1 \
                            or file_name.find('\\theme.mp4') != -1:
                        media_class_text = thread_db.db_media_class_by_uuid(
                            new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/trailers/') != -1 \
                                    or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['Movie Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                        elif media_class_text == 'TV Show' or media_class_text == 'TV Episode' \
                                or media_class_text == 'TV Season':
                            if file_name.find('/trailers/') != -1 \
                                    or file_name.find('\\trailers\\') != -1:
                                new_class_type_uuid = class_text_dict['TV Trailer']
                            else:
                                new_class_type_uuid = class_text_dict['TV Theme']
                    elif file_name.find('/extras/') != -1 or file_name.find('\\extras\\') != -1:
                        if thread_db.db_media_class_by_uuid(media_class_type_uuid) == 'Movie':
                            new_class_type_uuid = class_text_dict['Movie Extras']
                        elif thread_db.db_media_class_by_uuid(media_class_type_uuid) == 'TV Show' \
                                or thread_db.db_media_class_by_uuid(
                            media_class_type_uuid) == 'TV Episode' \
                                or media_class_text == 'TV Season':
                            new_class_type_uuid = class_text_dict['TV Extras']
                    elif file_name.find('/backdrops/') != -1 \
                            or file_name.find('\\backdrops\\') != -1:
                        media_class_text = thread_db.db_media_class_by_uuid(
                            new_class_type_uuid)
                        if media_class_text == 'Movie':
                            if file_name.find('/theme.mp3') != -1 \
                                    or file_name.find('\\theme.mp3') != -1 \
                                    or file_name.find('/theme.mp4') != -1 \
                                    or file_name.find('\\theme.mp4') != -1:
                                new_class_type_uuid = class_text_dict['Movie Theme']
                    # determine ffmpeg json data
                    if file_name[:1] == "\\":
                        file_name \
                            = file_name.replace('\\\\', 'smb://guest:\'\'@').replace('\\', '/')
                    # common_ffmpeg.com_ffmpeg_media_attr(file_name)
                    media_ffprobe_json = None
                # create media_json data
                media_json = json.dumps({'DateAdded': datetime.now().strftime("%Y-%m-%d"),
                                         'ChapterScan': True})
                media_id = str(uuid.uuid4())
                thread_db.db_insert_media(media_id, file_name,
                                          new_class_type_uuid, None, media_ffprobe_json, media_json)
                # Send a message so ffprobe runs
                channel.basic_publish(exchange='mkque_ffmpeg_ex',
                                      routing_key='mkffmpeg',
                                      body=json.dumps(
                                          {'Type': 'FFProbe', 'Data': media_id}),
                                      properties=pika.BasicProperties(content_type='text/plain',
                                                                      delivery_mode=1))
                if save_dl_record:
                    # media id begin and download que insert
                    thread_db.db_download_insert('Z', 0, json.dumps({'MediaID': media_id,
                                                                     'Path': file_name,
                                                                     'ClassID': new_class_type_uuid,
                                                                     'Status': None,
                                                                     'MetaNewID': str(uuid.uuid4()),
                                                                     'ProviderMetaID': None}))
        total_scanned += 1
        thread_db.db_audit_path_update_status(dir_guid,
                                              json.dumps({'Status': 'File scan: '
                                                                    + common_internationalization.com_inter_number_format(
                                                  total_scanned)
                                                                    + ' / ' + common_internationalization.com_inter_number_format(
                                                  total_file_in_dir),
                                                          'Pct': (
                                                                         total_scanned / total_file_in_dir) * 100}))
        thread_db.db_commit()
    common_global.es_inst.com_elastic_index('info',
                                            {'worker dir done': dir_path,
                                             'media class': media_class_type_uuid})
    # set to none so it doesn't show up
    thread_db.db_audit_path_update_status(dir_guid, None)
    if total_files > 0:
        thread_db.db_notification_insert(
            common_internationalization.com_inter_number_format(total_files)
            + " file(s) added from " + dir_path, True)
    thread_db.db_commit()
    thread_db.db_close()
    return


# fire off wait for it script to allow rabbitmq connection
wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                             'mkrabbitmq', '-p', ' 5672'], shell=False)
wait_pid.wait()

# Open a connection to RabbitMQ
parameters = pika.ConnectionParameters('mkrabbitmq',
                                       credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(parameters)

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue="mkffmpeg", durable=True,
                      exclusive=False, auto_delete=False)

# Turn on delivery confirmations
channel.confirm_delivery()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# load in all media from DB
global_known_media = []  # pylint: disable=C0103
known_media = db_connection.db_known_media()
# verify rows were returned
if known_media is not None:
    for media_row in known_media:
        if media_row['mm_media_path'] is not None:
            global_known_media.append(media_row['mm_media_path'])
known_media = None

# table the class_text into a dict...will lessen the db calls
class_text_dict = {}
for class_data in db_connection.db_media_class_list(None, None):
    class_text_dict[class_data['mm_media_class_type']
    ] = class_data['mm_media_class_guid']

# determine directories to audit
audit_directories = []  # pylint: disable=C0103
for row_data in db_connection.db_audit_paths():
    common_global.es_inst.com_elastic_index('info', {"Audit Path": str(row_data)})
    # check for UNC
    if row_data['mm_media_dir_path'][:1] == "\\":
        smb_stuff = common_network_cifs.CommonCIFSShare()
        addr, share, path \
            = common_string.com_string_unc_to_addr_path(row_data['mm_media_dir_path'])
        smb_stuff.com_cifs_connect(addr)
        if smb_stuff.com_cifs_share_directory_check(share, path):
            if datetime.strptime(time.ctime(
                    smb_stuff.com_cifs_share_file_dir_info(share, path).last_write_time),
                    "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'],
                                          str(row_data['mm_media_class_guid']),
                                          row_data['mm_media_dir_guid']))
                db_connection.db_audit_path_update_status(row_data['mm_media_dir_guid'],
                                                          json.dumps({'Status': 'Added to scan',
                                                                      'Pct': 100}))
        else:
            db_connection.db_notification_insert('UNC Library path not found: %s'
                                                 % row_data['mm_media_dir_path'], True)
        smb_stuff.com_cifs_close()
    else:
        # make sure the path still exists
        if not os.path.isdir(row_data['mm_media_dir_path']):
            db_connection.db_notification_insert('Library path not found: %s'
                                                 % row_data['mm_media_dir_path'], True)
        else:
            # verify the directory inodes has changed
            if datetime.strptime(time.ctime(os.path.getmtime(row_data['mm_media_dir_path'])),
                                 "%a %b %d %H:%M:%S %Y") > row_data['mm_media_dir_last_scanned']:
                audit_directories.append((row_data['mm_media_dir_path'],
                                          str(row_data['mm_media_class_guid']),
                                          row_data['mm_media_dir_guid']))
                db_connection.db_audit_path_update_status(row_data['mm_media_dir_guid'],
                                                          json.dumps({'Status': 'Added to scan',
                                                                      'Pct': 100}))

# commit
db_connection.db_commit()

# start processing the directories
if len(audit_directories) > 0:
    # switched to this since tracebacks work this method
    with futures.ThreadPoolExecutor(len(audit_directories)) as executor:
        futures = [executor.submit(worker, n) for n in audit_directories]
        for future in futures:
            pass
            # try:
            #     common_global.es_inst.com_elastic_index('info', {'future': str(future.result())})
            # except:
            #     pass

# commit
db_connection.db_commit()

# vaccum tables that had records added
db_connection.db_pgsql_vacuum_table('mm_media')
db_connection.db_pgsql_vacuum_table('mm_download_que')

# Cancel the consumer and return any pending messages
channel.cancel()
# close pika
channel.close()

# close the database
db_connection.db_close()
