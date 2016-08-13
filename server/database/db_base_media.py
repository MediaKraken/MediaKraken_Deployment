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
import logging
import uuid
import json
import datetime


# insert media into database
def srv_db_insert_media(self, media_uuid, media_path, media_class_uuid,\
        media_metadata_uuid, media_ffprobe_json, media_json):
    self.sql3_cursor.execute("insert into mm_media (mm_media_guid, mm_media_class_guid, mm_media_path, mm_media_metadata_guid, mm_media_ffprobe_json, mm_media_json) values (%s,%s,%s,%s,%s,%s)", (media_uuid, media_class_uuid, media_path, media_metadata_uuid, media_ffprobe_json, media_json))


# read in all media unless guid specified
def srv_db_read_media(self, media_guid=None):
    if media_guid is not None:
        self.sql3_cursor.execute("select * from mm_media where mm_media_guid = %s", (media_guid,))
        try:
            return self.sql3_cursor.fetchone()
        except:
            return None
    else:
        self.sql3_cursor.execute("select * from mm_media")
        return self.sql3_cursor.fetchall()


# count known media
def srv_db_known_media_count(self):
    self.sql3_cursor.execute('select count(*) from mm_media')
    return self.sql3_cursor.fetchone()[0]


# find all known media
def srv_db_known_media(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_media_path from mm_media order by mm_media_path')
    else:
        self.sql3_cursor.execute('select mm_media_path from mm_media where mm_media_guid in (select mm_media_guid from mm_media order by mm_media_path offset %s limit %s) order by mm_media_path', (offset, records))
    return self.sql3_cursor.fetchall()


# count matched media
def srv_db_matched_media_count(self):
    self.sql3_cursor.execute('select count(*) from mm_media where mm_media_metadata_guid is not NULL')
    return self.sql3_cursor.fetchone()[0]


# count all media that is NULL for meatadata match
def srv_db_known_media_All_Unmatched_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_media where mm_media_metadata_guid is NULL')
    return self.sql3_cursor.fetchone()[0]


# read all media that is NULL for metadata match
def srv_db_known_media_All_Unmatched(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_media_guid, mm_media_class_guid, mm_media_path from mm_media where mm_media_metadata_guid is NULL')
    else:
        self.sql3_cursor.execute('select mm_media_guid, mm_media_class_guid, mm_media_path from mm_media where mm_media_guid in (select mm_media_guid from mm_media where mm_media_metadata_guid is NULL offset %s limit %s) order by mm_media_path', (offset, records))
    return self.sql3_cursor.fetchall()


# count the duplicates for pagination
def srv_db_media_duplicate_count(self):
    self.sql3_cursor.execute('select count(*) from (select mm_media_metadata_guid from mm_media where mm_media_metadata_guid is not null group by mm_media_metadata_guid HAVING count(*) > 1) as total')
    return self.sql3_cursor.fetchone()[0]


# TODO subselect for speed
# list duplicates
def srv_db_media_duplicate(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_media_metadata_guid,mm_media_name,count(*) from mm_media,mm_metadata_movie where mm_media_metadata_guid is not null and mm_media_metadata_guid = mm_metadata_guid group by mm_media_metadata_guid,mm_media_name HAVING count(*) > 1 order by LOWER(mm_media_name)')
    else:
        self.sql3_cursor.execute('select mm_media_metadata_guid,mm_media_name,count(*) from mm_media,mm_metadata_movie where mm_media_metadata_guid is not null and mm_media_metadata_guid = mm_metadata_guid group by mm_media_metadata_guid,mm_media_name HAVING count(*) > 1 order by LOWER(mm_media_name) offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()


# duplicate detail count
def srv_db_media_duplicate_Detail_Count(self, guid):
    self.sql3_cursor.execute('select count(*) from mm_media where mm_media_metadata_guid = %s',\
        (guid,))
    return self.sql3_cursor.fetchall()


# list duplicate detail
def srv_db_media_duplicate_Detail(self, guid, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_media_guid,mm_media_path,mm_media_ffprobe_json from mm_media where mm_media_metadata_guid = %s', (guid,))
    else:
        self.sql3_cursor.execute('select mm_media_guid,mm_media_path,mm_media_ffprobe_json from mm_media where mm_media_guid in (select mm_media_guid from mm_media where mm_media_metadata_guid = %s offset %s limit %s)', (guid, offset, records))
    return self.sql3_cursor.fetchall()


# find path for media by uuid
def srv_db_media_path_by_uuid(self, media_uuid):
    self.sql3_cursor.execute('select mm_media_path from mm_media where mm_media_guid = %s',\
        (media_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_media_path']
    except:
        return None


# set watched/unwatched status for media
def srv_db_media_watched_status_update(self, media_guid, user_id, status_bool):
    # TODO   begin trans...as could update between these two commands
    # do this as a subselect instead....then don't have to worry about it
    self.sql3_cursor.execute('SELECT mm_media_json from mm_media where mm_media_guid = %s',\
        (media_guid,))
    json_data = self.sql3_cursor.fetchone()['mm_media_json']
    json_data.update({'UserStats': {user_id: {'Watched': status_bool}}})
    self.srv_db_update_media_json(media_guid, json.dumps(json_data))
    self.srv_db_Commit()


# set favorite status for media
def srv_db_media_favorite_status_update(self, media_guid, user_id, status_bool):
    # TODO   begin trans...as could update between these two commands
    # do this as a subselect instead....then don't have to worry about it
    self.sql3_cursor.execute('SELECT mm_media_json from mm_media where mm_media_guid = %s',\
        (media_guid,))
    json_data = self.sql3_cursor.fetchone()['mm_media_json']
    json_data.update({'UserStats': {user_id: {'Favorite': status_bool}}})
    self.srv_db_update_media_json(media_guid, json.dumps(json_data))
    self.srv_db_Commit()


# set favorite status for media
def srv_db_media_poo_status_update(self, media_guid, user_id, status_bool):
    # TODO   begin trans...as could update between these two commands
    # do this as a subselect instead....then don't have to worry about it
    self.sql3_cursor.execute('SELECT mm_media_json from mm_media where mm_media_guid = %s',
        (media_guid,))
    json_data = self.sql3_cursor.fetchone()['mm_media_json']
    json_data.update({'UserStats': {user_id: {'Poo': status_bool}}})
    self.srv_db_update_media_json(media_guid, json.dumps(json_data))
    self.srv_db_Commit()


# set mismatch status for media
def srv_db_media_mismatch_status_update(self, media_guid, user_id, status_bool):
    # TODO   begin trans...as could update between these two commands
    # do this as a subselect instead....then don't have to worry about it
    self.sql3_cursor.execute('SELECT mm_media_json from mm_media where mm_media_guid = %s',\
        (media_guid,))
    json_data = self.sql3_cursor.fetchone()['mm_media_json']
    json_data.update({'UserStats': {user_id: {'MisMatch': status_bool}}})
    self.srv_db_update_media_json(media_guid, json.dumps(json_data))
    self.srv_db_Commit()


# set checkpoint for media (so can pick up where left off per user)
def srv_db_media_watched_checkpoint_update(self, media_guid, user_id, ffmpeg_time):
    # TODO   begin trans...as could update between these two commands
    # do this as a subselect instead....then don't have to worry about it
    self.sql3_cursor.execute('SELECT mm_media_json from mm_media where mm_media_guid = %s',\
        (media_guid,))
    json_data = self.sql3_cursor.fetchone()['mm_media_json']
    json_data.update({'UserStats': {user_id: {'Checkpoint': ffmpeg_time}}})
    self.srv_db_update_media_json(media_guid, json.dumps(json_data))
    self.srv_db_Commit()


# update the mediaid
def srv_db_update_media_id(self, media_guid, metadata_guid):
    self.sql3_cursor.execute('update mm_media set mm_media_metadata_guid = %s where mm_media_guid = %s', (metadata_guid, media_guid))
    self.srv_db_Commit()


# update the mediajson
def srv_db_update_media_json(self, media_guid, mediajson):
    self.sql3_cursor.execute('update mm_media set mm_media_json = %s where mm_media_guid = %s',\
        (mediajson, media_guid))
    self.srv_db_Commit()


# return all media which needs chapter images created
def srv_db_known_media_Chapter_Scan(self):
    self.sql3_cursor.execute('select mm_media_guid, mm_media_json, mm_media_ffprobe_json, mm_media_path from mm_media where mm_media_json is null or mm_media_json->>\'ChapterScan\' = \'true\'')
    return self.sql3_cursor.fetchall()


# fetch all media with METADATA match
def srv_db_media_by_metadata_guid(self, metadata_guid):
    self.sql3_cursor.execute("select mm_media_name,mm_media_guid from mm_media,mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid and mm_media_metadata_guid = %s", (metadata_guid,))
    return self.sql3_cursor.fetchall()


# grab image path for media id NOT metadataid
def srv_db_media_image_path(self, media_id):
    self.sql3_cursor.execute("select mm_metadata_localimage_json->\'Images\' from mm_media, mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid and mm_media_guid = %s", (media_id,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_localimage_json']
    except:
        return None


# read in metadata by id
def srv_db_read_media_Metadata_Both(self, media_guid):
    self.sql3_cursor.execute("select mm_media_name,mm_media_metadata_guid,mm_media_ffprobe_json,mm_media_json,mm_metadata_json,mm_metadata_localimage_json,mm_metadata_media_id from mm_media, mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid and mm_media_guid = %s", (media_guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# do a like class path match for trailers and extras
def srv_db_read_media_Path_Like(self, media_path):
    sql_params = (media_path + '%'),  # use like since I won't be using the "root" directory but media within it
    self.sql3_cursor.execute("select mm_media_metadata_guid from mm_media where mm_media_path LIKE %s", sql_params)
    try:
        return self.sql3_cursor.fetchone()['mm_media_metadata_guid']
    except:
        return None


# new media count
def srv_db_read_media_New_Count(self, days_old=7):
    self.sql3_cursor.execute("select count(*) from mm_media, mm_metadata_movie, mm_media_class where mm_media_metadata_guid = mm_metadata_guid and mm_media.mm_media_class_guid = mm_media_class.mm_media_class_guid and mm_media_json->>\'DateAdded\' >= %s", ((datetime.datetime.now() - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"),))
    return self.sql3_cursor.fetchone()[0]


# TODO subselect for speed
# new media
def srv_db_read_media_New(self, days_old=7, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute("select mm_media_name, mm_media_guid, mm_media_class_type from mm_media, mm_metadata_movie, mm_media_class where mm_media_metadata_guid = mm_metadata_guid and mm_media.mm_media_class_guid = mm_media_class.mm_media_class_guid and mm_media_json->>\'DateAdded\' >= %s order by LOWER(mm_media_name), mm_media_class_type", ((datetime.datetime.now() - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"),))
    else:
        self.sql3_cursor.execute("select mm_media_name, mm_media_guid, mm_media_class_type from mm_media, mm_metadata_movie, mm_media_class where mm_media_metadata_guid = mm_metadata_guid and mm_media.mm_media_class_guid = mm_media_class.mm_media_class_guid and mm_media_json->>\'DateAdded\' >= %s order by LOWER(mm_media_name), mm_media_class_type offset %s limit %s", ((datetime.datetime.now() - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"), offset, records))
    return self.sql3_cursor.fetchall()
