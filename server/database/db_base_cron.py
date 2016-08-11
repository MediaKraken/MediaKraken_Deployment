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
import json
import datetime


# return cron count
def MK_Server_Database_Cron_List_Count(self, enabled_only=False):
    if not enabled_only:
        self.sql3_cursor.execute('select count(*) from mm_cron')
    else:
        self.sql3_cursor.execute('select count(*) from mm_cron where mm_cron_enabled = true')
    return self.sql3_cursor.fetchone()[0]


# return cron list
def MK_Server_Database_Cron_List(self, enabled_only=False, offset=None, records=None):
    if offset is None:
        if not enabled_only:
            self.sql3_cursor.execute('select mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path from mm_cron order by mm_cron_name')
        else:
            self.sql3_cursor.execute('select mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path from mm_cron where mm_cron_enabled = true order by mm_cron_name')
    else:
        if not enabled_only:
            self.sql3_cursor.execute('select mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path from mm_cron where mm_cron_guid in (select mm_cron_guid from mm_cron order by mm_cron_name offset %s limit %s) order by mm_cron_name', (offset, records))
        else:
            self.sql3_cursor.execute('select mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path from mm_cron where mm_cron_guid in (select mm_cron_guid from mm_cron where mm_cron_enabled = true order by mm_cron_name offset %s limit %s) order by mm_cron_name', (offset, records))
    return self.sql3_cursor.fetchall()


# update cron run date
def MK_Server_Database_Cron_Time_Update(self, cron_type):
    self.sql3_cursor.execute('update mm_cron set mm_cron_last_run = %s where mm_cron_name = %s', (datetime.datetime.now(), cron_type))
