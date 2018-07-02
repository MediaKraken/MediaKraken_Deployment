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

import datetime
import json

from common import common_global


def db_insert_media(self, media_uuid, media_path, media_class_uuid,
                    media_metadata_uuid, media_ffprobe_json, media_json):
    """
    # insert media into database
    """
    self.db_cursor.execute('insert into mm_media (mm_media_guid, mm_media_class_guid,'
                           ' mm_media_path, mm_media_metadata_guid, mm_media_ffprobe_json,'
                           ' mm_media_json) values (%s,%s,%s,%s,%s,%s)',
                           (media_uuid, media_class_uuid, media_path,
                            media_metadata_uuid, media_ffprobe_json, media_json))
    self.db_commit()


def db_read_media(self, media_guid=None):
    """
    # read in all media unless guid specified
    """
    if media_guid is not None:
        self.db_cursor.execute(
            'select * from mm_media where mm_media_guid = %s', (media_guid,))
        try:
            return self.db_cursor.fetchone()
        except:
            return None
    else:
        self.db_cursor.execute('select * from mm_media')
        return self.db_cursor.fetchall()


def db_known_media_count(self):
    """
    # count known media
    """
    self.db_cursor.execute('select count(*) from mm_media')
    return self.db_cursor.fetchone()[0]


def db_known_media(self, offset=None, records=None):
    """
    # find all known media
    """
    if offset is None:
        self.db_cursor.execute(
            'select mm_media_path from mm_media order by mm_media_path')
    else:
        self.db_cursor.execute('select mm_media_path from mm_media where mm_media_guid'
                               ' in (select mm_media_guid from mm_media order by mm_media_path'
                               ' offset %s limit %s) order by mm_media_path', (offset, records))
    return self.db_cursor.fetchall()


def db_matched_media_count(self):
    """
    # count matched media
    """
    self.db_cursor.execute('select count(*) from mm_media'
                           ' where mm_media_metadata_guid is not NULL')
    return self.db_cursor.fetchone()[0]


def db_known_media_all_unmatched_count(self):
    """
    # count all media that is NULL for meatadata match
    """
    self.db_cursor.execute(
        'select count(*) from mm_media where mm_media_metadata_guid is NULL')
    return self.db_cursor.fetchone()[0]


def db_known_media_all_unmatched(self, offset=None, records=None):
    """
    # read all media that is NULL for metadata match
    """
    if offset is None:
        self.db_cursor.execute('select mm_media_guid, mm_media_class_guid, mm_media_path'
                               ' from mm_media where mm_media_metadata_guid is NULL')
    else:
        self.db_cursor.execute('select mm_media_guid, mm_media_class_guid, mm_media_path'
                               ' from mm_media where mm_media_guid'
                               ' in (select mm_media_guid from mm_media'
                               ' where mm_media_metadata_guid is NULL offset %s limit %s)'
                               ' order by mm_media_path', (offset, records))
    return self.db_cursor.fetchall()


def db_media_duplicate_count(self):
    """
    # count the duplicates for pagination
    """
    # TODO technically this will "dupe" things like subtitles atm
    self.db_cursor.execute('select count(*) from (select mm_media_metadata_guid'
                           ' from mm_media where mm_media_metadata_guid is not null'
                           ' group by mm_media_metadata_guid HAVING count(*) > 1) as total')
    return self.db_cursor.fetchone()[0]


# TODO subselect for speed
def db_media_duplicate(self, offset=None, records=None):
    """
    # list duplicates
    """
    # TODO technically this will "dupe" things like subtitles atm
    if offset is None:
        self.db_cursor.execute('select mm_media_metadata_guid,mm_media_name,count(*)'
                               ' from mm_media,mm_metadata_movie'
                               ' where mm_media_metadata_guid is not null'
                               ' and mm_media_metadata_guid = mm_metadata_guid'
                               ' group by mm_media_metadata_guid,'
                               'mm_media_name HAVING count(*) > 1 order by LOWER(mm_media_name)')
    else:
        self.db_cursor.execute('select mm_media_metadata_guid,mm_media_name,count(*)'
                               ' from mm_media,mm_metadata_movie'
                               ' where mm_media_metadata_guid is not null'
                               ' and mm_media_metadata_guid = mm_metadata_guid'
                               ' group by mm_media_metadata_guid,'
                               ' mm_media_name HAVING count(*) > 1 order by LOWER(mm_media_name)'
                               ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_media_duplicate_detail_count(self, guid):
    """
    # duplicate detail count
    """
    self.db_cursor.execute('select count(*) from mm_media where mm_media_metadata_guid = %s',
                           (guid,))
    return self.db_cursor.fetchall()


def db_media_duplicate_detail(self, guid, offset=None, records=None):
    """
    # list duplicate detail
    """
    if offset is None:
        self.db_cursor.execute('select mm_media_guid,mm_media_path,mm_media_ffprobe_json'
                               ' from mm_media where mm_media_metadata_guid = %s', (guid,))
    else:
        self.db_cursor.execute('select mm_media_guid,mm_media_path,mm_media_ffprobe_json'
                               ' from mm_media where mm_media_guid'
                               ' in (select mm_media_guid from mm_media'
                               ' where mm_media_metadata_guid = %s offset %s limit %s)',
                               (guid, offset, records))
    return self.db_cursor.fetchall()


def db_media_path_by_uuid(self, media_uuid):
    """
    # find path for media by uuid
    """
    self.db_cursor.execute('select mm_media_path from mm_media where mm_media_guid = %s',
                           (media_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_media_path']
    except:
        return None


def db_media_rating_update(self, media_guid, user_id, status_text):
    """
    # set favorite status for media
    """
    self.db_cursor.execute('SELECT mm_media_json from mm_media'
                           ' where mm_media_guid = %s FOR UPDATE', (media_guid,))
    if status_text == 'watched' or status_text == 'mismatch':
        status_setting = True
    else:
        status_setting = status_text
        status_text = 'Rating'
    try:
        json_data = self.db_cursor.fetchone()['mm_media_json']
        if 'UserStats' not in json_data:
            json_data['UserStats'] = {}
        if user_id in json_data['UserStats']:
            json_data['UserStats'][user_id][status_text] = status_setting
        else:
            json_data['UserStats'][user_id] = {status_text: status_setting}
        self.db_update_media_json(media_guid, json.dumps(json_data))
        self.db_commit()
    except:
        self.db_rollback()
        return None


def db_media_watched_checkpoint_update(self, media_guid, user_id, ffmpeg_time):
    """
    # set checkpoint for media (so can pick up where left off per user)
    """
    self.db_cursor.execute('SELECT mm_media_json from mm_media'
                           ' where mm_media_guid = %s FOR UPDATE', (media_guid,))
    try:
        json_data = self.db_cursor.fetchone()['mm_media_json']
        if 'UserStats' not in json_data:
            json_data['UserStats'] = {}
        if user_id in json_data['UserStats']:
            json_data['UserStats'][user_id]['ffmpeg_checkpoint'] = ffmpeg_time
        else:
            json_data['UserStats'][user_id] = {
                'ffmpeg_checkpoint': ffmpeg_time}
        self.db_update_media_json(media_guid, json.dumps(json_data))
        self.db_commit()
    except:
        self.db_rollback()
        return None


def db_update_media_id(self, media_guid, metadata_guid):
    """
    # update the mediaid
    """
    self.db_cursor.execute('update mm_media set mm_media_metadata_guid = %s'
                           ' where mm_media_guid = %s', (metadata_guid, media_guid))
    self.db_commit()


def db_update_media_json(self, media_guid, mediajson):
    """
    # update the mediajson
    """
    self.db_cursor.execute('update mm_media set mm_media_json = %s where mm_media_guid = %s',
                           (mediajson, media_guid))
    self.db_commit()


def db_known_media_chapter_scan(self):
    """
    # return all media which needs chapter images created
    """
    self.db_cursor.execute('select mm_media_guid, mm_media_json, mm_media_ffprobe_json,'
                           ' mm_media_path from mm_media where mm_media_json is null'
                           ' or mm_media_json->>\'ChapterScan\' = \'true\'')
    return self.db_cursor.fetchall()


def db_media_by_metadata_guid(self, metadata_guid, media_class_type):
    """
    # fetch all media with METADATA match
    """
    self.db_cursor.execute('select mm_media_name,mm_media_guid from mm_media,'
                           'mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid'
                           ' and mm_media_metadata_guid = %s',
                            (metadata_guid, media_class_type))
    return self.db_cursor.fetchall()


def db_media_image_path(self, media_id):
    """
    # grab image path for media id NOT metadataid
    """
    self.db_cursor.execute('select mm_metadata_localimage_json->\'Images\' from mm_media,'
                           ' mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid'
                           ' and mm_media_guid = %s', (media_id,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_localimage_json']
    except:
        return None


def db_read_media_metadata_both(self, media_guid):
    """
    # read in metadata by id
    """
    self.db_cursor.execute('select mm_media_name,mm_media_metadata_guid,mm_media_ffprobe_json,'
                           'mm_media_json,mm_metadata_json,mm_metadata_localimage_json,'
                           'mm_metadata_media_id from mm_media, mm_metadata_movie'
                           ' where mm_media_metadata_guid = mm_metadata_guid'
                           ' and mm_media_guid = %s', (media_guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_read_media_path_like(self, media_path):
    """
    # do a like class path match for trailers and extras
    """
    # use like since I won't be using the "root" directory but media within it
    common_global.es_inst.com_elastic_index('info', {'path like': media_path})
    self.db_cursor.execute('select mm_media_metadata_guid from mm_media'
                           ' where mm_media_path LIKE %s'
                           ' and mm_media_metadata_guid IS NOT NULL limit 1',
                           ((media_path + '%'),))
    try:
        return self.db_cursor.fetchone()['mm_media_metadata_guid']
    except:
        return None


def db_read_media_new_count(self, days_old=7):
    """
    # new media count
    """
    self.db_cursor.execute('select count(*) from mm_media, mm_metadata_movie, mm_media_class'
                           ' where mm_media_metadata_guid = mm_metadata_guid'
                           ' and mm_media.mm_media_class_guid ='
                           ' mm_media_class.mm_media_class_guid'
                           ' and mm_media_json->>\'DateAdded\' >= %s',
                           ((datetime.datetime.now()
                             - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"),))
    return self.db_cursor.fetchone()[0]


# TODO subselect for speed
def db_read_media_new(self, days_old=7, offset=None, records=None):
    """
    # new media
    """
    if offset is None:
        self.db_cursor.execute('select mm_media_name, mm_media_guid, mm_media_class_type'
                               ' from mm_media, mm_metadata_movie, mm_media_class'
                               ' where mm_media_metadata_guid = mm_metadata_guid'
                               ' and mm_media.mm_media_class_guid'
                               ' = mm_media_class.mm_media_class_guid'
                               ' and mm_media_json->>\'DateAdded\' >= %s'
                               ' order by LOWER(mm_media_name),'
                               ' mm_media_class_type',
                               ((datetime.datetime.now()
                                 - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"),))
    else:
        self.db_cursor.execute('select mm_media_name, mm_media_guid, mm_media_class_type'
                               ' from mm_media, mm_metadata_movie, mm_media_class'
                               ' where mm_media_metadata_guid = mm_metadata_guid'
                               ' and mm_media.mm_media_class_guid'
                               ' = mm_media_class.mm_media_class_guid'
                               ' and mm_media_json->>\'DateAdded\' >= %s'
                               ' order by LOWER(mm_media_name),'
                               ' mm_media_class_type offset %s limit %s',
                               ((datetime.datetime.now()
                                 - datetime.timedelta(days=days_old)).strftime("%Y-%m-%d"),
                                offset, records))
    return self.db_cursor.fetchall()


def db_read_media_ffprobe(self):
    """
    Read in all media that needs ffprobe
    """
    self.db_cursor.execute('select mm_media_guid,b from mm_media'
                           ' where mm_media_ffprobe_json is NULL')
    return self.db_cursor.fetchall()


def db_media_ffmeg_update(self, media_guid, ffmpeg_json):
    """
    Update the ffprobe json data
    """
    self.db_cursor.execute('update mm_media set mm_media_ffprobe_json = %s'
                           ' where mm_media_guid = %s', (ffmpeg_json, media_guid))
    self.db_commit()
