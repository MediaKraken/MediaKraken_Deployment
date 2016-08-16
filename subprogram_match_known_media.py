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
# prep totals
files_to_id = 0
files_added = 0
build_collection = False


total_media_to_match = db.srv_db_known_media_All_Unmatched_Count()
# begin the media match on NULL matches
for row_data in db.srv_db_known_media_All_Unmatched():
    files_to_id += 1
    # lookup class from db
    metadata_uuid = None
    if row_data['mm_media_class_guid'] is not None:
        try:
            logging.debug("class_uuid: %s %s", row_data['mm_media_class_guid'],\
                row_data['mm_media_path'])
        except:
            logging.debug("unable to print file")
    metadata_uuid = metadata_identification(db_connection, row_data['mm_media_class_guid'],\
        row_data['mm_media_path'])
    # update the media row with the json media id AND THE proper NAME!!!
    if metadata_uuid is not None:
        logging.debug("update: %s %s", row_data['mm_media_guid'], metadata_uuid)
        db.srv_db_update_media_id(row_data['mm_media_guid'], metadata_uuid)
        files_added += 1
    db.srv_db_Option_Status_Update_Scan_Json(json.dumps({'Status': 'Media lookup: '
        + locale.format('%d', files_to_id, True) + ' / '\
        + locale.format('%d', total_media_to_match, True),\
        'Pct': (files_to_id / total_media_to_match) * 100}))
    db.srv_db_commit()


# send notications
if files_to_id > 0:
    db.srv_db_Notification_Insert(locale.format('%d', files_to_id, True)\
        + " file(s) scanned.", True)
if files_added > 0:
    db.srv_db_Notification_Insert(locale.format('%d', files_added, True)\
        + " new media file(s) matched.", True)
if build_collection:
    db.srv_db_trigger_insert(('python', './subprogram_update_create_collections.py'))
