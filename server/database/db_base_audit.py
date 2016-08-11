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
import datetime
import psycopg2


# read scan status
def MK_Server_Database_Audit_Path_Status(self):
    self.sql3_cursor.execute("select mm_media_dir_path, mm_media_dir_status from mm_media_dir where mm_media_dir_status IS NOT NULL order by mm_media_dir_path")
    return self.sql3_cursor.fetchall()


# update status
def MK_Server_Database_Audit_Path_Update_Status(self, lib_guid, status_json):
    self.sql3_cursor.execute("update mm_media_dir set mm_media_dir_status = %s where mm_media_dir_guid = %s", (status_json, lib_guid,))


# read the paths to audit
def MK_Server_Database_Audit_Paths_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_media_dir')
    return self.sql3_cursor.fetchone()[0]


# update audit path
def MK_Server_Database_Audit_Path_Update_By_UUID(self, lib_path, class_guid, lib_guid):
    self.sql3_cursor.execute("update mm_media_dir set mm_media_dir_path = %s, mm_media_dir_class_type = %s where mm_media_dir_guid = %s", ())


# remove media path
def MK_Server_Database_Audit_Path_Delete(self, lib_guid):
    self.sql3_cursor.execute(u"delete from mm_media_dir where mm_media_dir_guid = %s", (lib_guid,))


# add media path
def MK_Server_Database_Audit_Path_Add(self, dir_path, class_guid):
    self.sql3_cursor.execute("insert into mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned) values (%s,%s,%s,%s)", (str(uuid.uuid4()), dir_path, class_guid, psycopg2.Timestamp(1970, 1, 1, 0, 0, 1)))


# lib path check (dupes)
def MK_Server_Database_Audit_Path_Check(self, dir_path):
    self.sql3_cursor.execute('select count(*) from mm_media_dir where mm_media_dir_path = %s',\
        (dir_path,))
    return self.sql3_cursor.fetchone()[0]


# update the timestamp for directory scans
def MK_Server_Database_Audit_Directory_Timestamp_Update(self, file_path):
    self.sql3_cursor.execute('update mm_media_dir set mm_media_dir_last_scanned = %s where mm_media_dir_path = %s', (datetime.datetime.now(), file_path))


# TODO subselect speed
# read the paths to audit
def MK_Server_Database_Audit_Paths(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_media_dir_path, mm_media_class_type, mm_media_dir_last_scanned, mm_media_class_guid, mm_media_dir_guid from mm_media_dir, mm_media_class where mm_media_dir_class_type = mm_media_class_guid order by mm_media_class_type, mm_media_dir_path')
    else:
        self.sql3_cursor.execute('select mm_media_dir_path, mm_media_class_type, mm_media_dir_last_scanned, mm_media_class_guid, mm_media_dir_guid from mm_media_dir, mm_media_class where mm_media_dir_class_type = mm_media_class_guid order by mm_media_class_type, mm_media_dir_path offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()


# lib data per id
def MK_Server_Database_Audit_Path_By_UUID(self, dir_id):
    self.sql3_cursor.execute('select mm_media_dir_guid,mm_media_dir_path,mm_media_dir_class_type from mm_media_dir where mm_media_dir_guid = %s', (dir_id,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None
