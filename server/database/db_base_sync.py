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


def srv_db_sync_list_count(self):
    """
    # return count of sync jobs
    """
    self.sql3_cursor.execute('select count(*) from mm_sync')
    return self.sql3_cursor.fetchone()[0]


def srv_db_sync_list(self, offset=None, records=None, user_guid=None):
    """
    # return list of sync jobs
    """
    if user_guid is None:
        # complete list for admins
        if offset is None:
            self.sql3_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'\
                ' mm_sync_options_json from mm_sync'\
                ' order by mm_sync_options_json->\'Priority\' desc, mm_sync_path')
        else:
            self.sql3_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'\
                ' mm_sync_options_json from mm_sync where mm_sync_guid in (select mm_sync_guid'\
                ' from mm_sync order by mm_sync_options_json->\'Priority\' desc, mm_sync_path'\
                ' offset %s limit %s) order by mm_sync_options_json->\'Priority\''\
                ' desc, mm_sync_path', (offset, records))
    else:
        if offset is None:
            self.sql3_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'\
                ' mm_sync_options_json from mm_sync where mm_sync_options_json->\'User\' ? %s'\
                ' order by mm_sync_options_json->\'Priority\' desc, mm_sync_path')
        else:
            self.sql3_cursor.execute('select mm_sync_guid uuid, mm_sync_path, mm_sync_path_to,'\
                ' mm_sync_options_json from mm_sync where mm_sync_guid in (select mm_sync_guid'\
                ' from mm_sync where mm_sync_options_json->\'User\' ? %s'\
                ' order by mm_sync_options_json->\'Priority\' desc, mm_sync_path'\
                ' offset %s limit %s) order by mm_sync_options_json->\'Priority\''\
                ' desc, mm_sync_path', (user_guid, offset, records))
    return self.sql3_cursor.fetchall()


def srv_db_sync_insert(self, sync_path, sync_path_to, sync_json):
    """
    # insert sync job
    """
    self.sql3_cursor.execute('insert into mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to,'\
        ' mm_sync_options_json) values (%s, %s, %s, %s)', (str(uuid.uuid4()), sync_path,\
        sync_path_to, sync_json))


def srv_db_sync_delete(self, sync_guid):
    """
    # delete sync job
    """
    self.sql3_cursor.execute('delete from mm_sync where mm_sync_guid = %s', (sync_guid,))


def srv_db_sync_progress_update(self, sync_guid, sync_percent):
    """
    # update progress
    """
    self.sql3_cursor.execute('update mm_sync set mm_sync_options_json->\'Progress\' = %s'\
        ' where mm_sync_guid = %', (sync_percent, sync_guid))
