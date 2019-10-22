"""
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
"""

import datetime
import os
import uuid

import psycopg2


def db_audit_path_status(self):
    """
    # read scan status
    """
    self.db_cursor.execute('select mm_media_dir_path,'
                           ' mm_media_dir_status'
                           ' from mm_media_dir'
                           ' where mm_media_dir_status IS NOT NULL order by mm_media_dir_path')
    return self.db_cursor.fetchall()


def db_audit_path_update_status(self, lib_guid, status_json):
    """
    # update status
    """
    self.db_cursor.execute('update mm_media_dir set mm_media_dir_status = %s'
                           ' where mm_media_dir_guid = %s', (status_json, lib_guid))


def db_audit_path_update_by_uuid(self, lib_path, class_guid, lib_guid):
    """
    # update audit path
    """
    self.db_cursor.execute('update mm_media_dir set mm_media_dir_path = %s,'
                           ' mm_media_dir_class_type = %s'
                           ' where mm_media_dir_guid = %s',
                           (lib_path, class_guid, lib_guid))


def db_audit_path_delete(self, lib_guid):
    """
    # remove media path
    """
    self.db_cursor.execute(
        'delete from mm_media_dir where mm_media_dir_guid = %s', (lib_guid,))


def db_audit_path_add(self, dir_path, class_guid, share_guid):
    """
    # add media path
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_media_dir (mm_media_dir_guid,'
                           ' mm_media_dir_path,'
                           ' mm_media_dir_class_type,'
                           ' mm_media_dir_last_scanned,'
                           ' mm_media_dir_share_guid)'
                           ' values (%s,%s,%s,%s,%s)',
                           (new_guid, dir_path, class_guid,
                            psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), share_guid))
    return new_guid


def db_audit_path_check(self, dir_path):
    """
    # lib path check (dupes)
    """
    self.db_cursor.execute('select count(*) from mm_media_dir where mm_media_dir_path = %s',
                           (dir_path,))
    return self.db_cursor.fetchone()[0]


def db_audit_dir_timestamp_update(self, dir_path):
    """
    # update the timestamp for directory scans
    """
    if dir_path[:1] != "\\":  # if not unc.....add the mnt
        dir_path = os.path.join('/mediakraken/mnt', dir_path)
    self.db_cursor.execute('update mm_media_dir set mm_media_dir_last_scanned = %s'
                           ' where mm_media_dir_path = %s', (datetime.datetime.now(), dir_path))


def db_audit_paths(self, offset=0, records=None):
    """
    # read the paths to audit
    """
    self.db_cursor.execute('select mm_media_dir_path,'
                           ' mm_media_class_type,'
                           ' mm_media_dir_last_scanned,'
                           ' mm_media_class_guid,'
                           ' mm_media_dir_guid'
                           ' from mm_media_dir'
                           ' order by mm_media_class_type, mm_media_dir_path'
                           ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_audit_path_by_uuid(self, dir_id):
    """
    # lib data per id
    """
    self.db_cursor.execute('select mm_media_dir_guid,'
                           ' mm_media_dir_path,'
                           ' mm_media_dir_class_type'
                           ' from mm_media_dir'
                           ' where mm_media_dir_guid = %s', (dir_id,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_audit_shares(self, offset=0, records=None):
    """
    # read the shares list
    """
    self.db_cursor.execute('select mm_media_share_guid,'
                           ' mm_media_share_type,'
                           ' mm_media_share_user,'
                           ' mm_media_share_password,'
                           ' mm_media_share_server,'
                           ' mm_media_share_path'
                           ' from mm_media_share'
                           ' order by mm_media_share_type, mm_media_share_server,'
                           ' mm_media_share_path offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_audit_share_delete(self, share_guid):
    """
    # remove share
    """
    self.db_cursor.execute('delete from mm_media_share where mm_media_share_guid = %s',
                           (share_guid,))


def db_audit_share_by_uuid(self, share_id):
    """
    # share per id
    """
    self.db_cursor.execute('select mm_media_share_guid,'
                           ' mm_media_share_type,'
                           ' mm_media_share_user,'
                           ' mm_media_share_password,'
                           ' mm_media_share_server,'
                           ' mm_media_share_path,'
                           ' from mm_media_share'
                           ' where mm_media_share_guid = %s', (share_id,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_audit_share_update_by_uuid(self, share_type, share_user, share_password, share_server,
                                  share_path, share_id):
    """
    # update share
    """
    self.db_cursor.execute('update mm_media_share set mm_media_share_type = %s,'
                           ' mm_media_share_user = %s,'
                           ' mm_media_share_password = %s',
                           ' mm_media_share_server = %s',
                           ' where mm_media_share_path = %s',
                           ' and mm_media_share_guid = %s',
                           (share_type, share_user, share_password, share_server,
                            share_path, share_id))


def db_audit_share_check(self, dir_path):
    """
    # share path check (dupes)
    """
    self.db_cursor.execute('select count(*) from mm_media_share where mm_media_share_path = %s',
                           (dir_path,))
    return self.db_cursor.fetchone()[0]


def db_audit_share_add(self, share_type, share_user, share_password, share_server, share_path):
    """
    # add share path
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_media_share (mm_media_share_guid,'
                           ' mm_media_share_type,'
                           ' mm_media_share_user,'
                           ' mm_media_share_password,'
                           ' mm_media_share_server,'
                           ' mm_media_share_path)'
                           ' values (%s,%s,%s,%s,%s,%s)',
                           (new_guid, share_type, share_user,
                            share_password, share_server, share_path))
    return new_guid
