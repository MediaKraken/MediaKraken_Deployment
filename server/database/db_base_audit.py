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
#import logging
import uuid
import datetime
import psycopg2


def srv_db_audit_path_status(self):
    """
    # read scan status
    """
    self.db_cursor.execute('select mm_media_dir_path, mm_media_dir_status from mm_media_dir'\
        ' where mm_media_dir_status IS NOT NULL order by mm_media_dir_path')
    return self.db_cursor.fetchall()


def srv_db_audit_path_update_status(self, lib_guid, status_json):
    """
    # update status
    """
    self.db_cursor.execute('update mm_media_dir set mm_media_dir_status = %s'\
        ' where mm_media_dir_guid = %s', (status_json, lib_guid,))


def srv_db_audit_paths_count(self):
    """
    # read the paths to audit
    """
    self.db_cursor.execute('select count(*) from mm_media_dir')
    return self.db_cursor.fetchone()[0]


def srv_db_audit_path_update_by_uuid(self, lib_path, class_guid, lib_guid):
    """
    # update audit path
    """
    self.db_cursor.execute'"update mm_media_dir set mm_media_dir_path = %s,'\
        ' mm_media_dir_class_type = %s where mm_media_dir_guid = %s', ())


def srv_db_audit_path_delete(self, lib_guid):
    """
    # remove media path
    """
    self.db_cursor.execute('delete from mm_media_dir where mm_media_dir_guid = %s', (lib_guid,))


def srv_db_audit_path_add(self, dir_path, class_guid):
    """
    # add media path
    """
    self.db_cursor.execute('insert into mm_media_dir (mm_media_dir_guid, mm_media_dir_path,'\
        ' mm_media_dir_class_type, mm_media_dir_last_scanned) values (%s,%s,%s,%s)',\
        (str(uuid.uuid4()), dir_path, class_guid, psycopg2.Timestamp(1970, 1, 1, 0, 0, 1)))


def srv_db_audit_path_check(self, dir_path):
    """
    # lib path check (dupes)
    """
    self.db_cursor.execute('select count(*) from mm_media_dir where mm_media_dir_path = %s',\
        (dir_path,))
    return self.db_cursor.fetchone()[0]


def srv_db_audit_directory_timestamp_update(self, file_path):
    """
    # update the timestamp for directory scans
    """
    self.db_cursor.execute('update mm_media_dir set mm_media_dir_last_scanned = %s'\
        ' where mm_media_dir_path = %s', (datetime.datetime.now(), file_path))


# TODO subselect speed
def srv_db_audit_paths(self, offset=None, records=None):
    """
    # read the paths to audit
    """
    if offset is None:
        self.db_cursor.execute('select mm_media_dir_path, mm_media_class_type,'\
            ' mm_media_dir_last_scanned, mm_media_class_guid, mm_media_dir_guid'\
            ' from mm_media_dir, mm_media_class where mm_media_dir_class_type ='\
            ' mm_media_class_guid order by mm_media_class_type, mm_media_dir_path')
    else:
        self.db_cursor.execute('select mm_media_dir_path, mm_media_class_type,'\
            ' mm_media_dir_last_scanned, mm_media_class_guid, mm_media_dir_guid'\
            ' from mm_media_dir, mm_media_class where mm_media_dir_class_type'\
            ' = mm_media_class_guid order by mm_media_class_type, mm_media_dir_path'\
            ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def srv_db_audit_path_by_uuid(self, dir_id):
    """
    # lib data per id
    """
    self.db_cursor.execute('select mm_media_dir_guid,mm_media_dir_path,mm_media_dir_class_type'\
        ' from mm_media_dir where mm_media_dir_guid = %s', (dir_id,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None
