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

import uuid


def db_sync_list_count(self):
    """
    # return count of sync jobs
    """
    self.db_cursor.execute('select count(*) from mm_sync')
    return self.db_cursor.fetchone()[0]


def db_sync_list(self, offset=0, records=None, user_guid=None):
    """
    # return list of sync jobs
    """
    # TODO by priority, name, year
    if user_guid is None:
        # complete list for admins
        self.db_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'
                               ' mm_sync_options_json from mm_sync'
                               ' where mm_sync_guid in (select mm_sync_guid'
                               ' from mm_sync order by mm_sync_options_json->\'Priority\''
                               ' desc, mm_sync_path'
                               ' offset %s limit %s)'
                               ' order by mm_sync_options_json->\'Priority\''
                               ' desc, mm_sync_path', (offset, records))
    else:
        self.db_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'
                               ' mm_sync_options_json from mm_sync'
                               ' where mm_sync_guid in (select mm_sync_guid'
                               ' from mm_sync where mm_sync_options_json->\'User\'::text = %s'
                               ' order by mm_sync_options_json->\'Priority\''
                               ' desc, mm_sync_path  offset %s limit %s)'
                               ' order by mm_sync_options_json->\'Priority\''
                               ' desc, mm_sync_path', (str(user_guid), offset, records))
    return self.db_cursor.fetchall()


def db_sync_insert(self, sync_path, sync_path_to, sync_json):
    """
    # insert sync job
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to,'
                           ' mm_sync_options_json) values (%s, %s, %s, %s)', (new_guid, sync_path,
                                                                              sync_path_to,
                                                                              sync_json))
    self.db_commit()
    return new_guid


def db_sync_delete(self, sync_guid):
    """
    # delete sync job
    """
    self.db_cursor.execute(
        'delete from mm_sync where mm_sync_guid = %s', (sync_guid,))
    self.db_commit()


def db_sync_progress_update(self, sync_guid, sync_percent):
    """
    # update progress
    """
    self.db_cursor.execute('update mm_sync set mm_sync_options_json->\'Progress\' = %s'
                           ' where mm_sync_guid = %', (sync_percent, sync_guid))
    self.db_commit()
