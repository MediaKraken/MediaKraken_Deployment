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
import uuid


def db_cron_insert(self, cron_name, cron_desc, cron_enabled, cron_schedule, cron_last_run,
                   cron_json):
    """
    insert cron job
    """
    new_cron_id = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_cron (mm_cron_guid,'
                           ' mm_cron_name,'
                           ' mm_cron_description,'
                           ' mm_cron_enabled,'
                           ' mm_cron_schedule,'
                           ' mm_cron_last_run, mm_cron_json)'
                           ' values (%s,%s,%s,%s,%s,%s,%s)',
                           (new_cron_id, cron_name, cron_desc, cron_enabled, cron_schedule,
                            cron_last_run, cron_json))
    return new_cron_id


def db_cron_list_count(self, enabled_only=False):
    """
    Return number of cron jobs
    """
    if not enabled_only:
        self.db_cursor.execute('select count(*) from mm_cron')
    else:
        self.db_cursor.execute(
            'select count(*) from mm_cron'
            ' where mm_cron_enabled = true')
    return self.db_cursor.fetchone()[0]


def db_cron_list(self, enabled_only=False, offset=0, records=None):
    """
    Return cron list
    """
    if not enabled_only:
        self.db_cursor.execute('select mm_cron_guid,'
                               ' mm_cron_name,'
                               ' mm_cron_description,'
                               ' mm_cron_enabled,'
                               ' mm_cron_schedule,'
                               ' mm_cron_last_run,'
                               ' mm_cron_json'
                               ' from mm_cron where mm_cron_guid'
                               ' in (select mm_cron_guid from mm_cron'
                               ' order by mm_cron_name offset %s limit %s)'
                               ' order by mm_cron_name', (offset, records))
    else:
        self.db_cursor.execute('select mm_cron_guid,'
                               ' mm_cron_name,'
                               ' mm_cron_description,'
                               ' mm_cron_enabled,'
                               ' mm_cron_schedule,'
                               ' mm_cron_last_run,'
                               ' mm_cron_json'
                               ' from mm_cron where mm_cron_guid'
                               ' in (select mm_cron_guid from mm_cron'
                               ' where mm_cron_enabled = true'
                               ' order by mm_cron_name offset %s limit %s)'
                               ' order by mm_cron_name', (offset, records))
    return self.db_cursor.fetchall()


def db_cron_time_update(self, cron_type):
    """
    Update the datetime in which a cron job was run
    """
    self.db_cursor.execute('update mm_cron set mm_cron_last_run = %s'
                           ' where mm_cron_name = %s',
                           (datetime.datetime.now(), cron_type))


def db_cron_delete(self, cron_uuid):
    """
    Delete cron job
    """
    self.db_cursor.execute('delete from mm_cron'
                           ' where mm_cron_guid = %s',
                           (cron_uuid,))


def db_cron_info(self, cron_uuid):
    """
    Cron job info
    """
    self.db_cursor.execute('select mm_cron_guid,'
                           ' mm_cron_name,'
                           ' mm_cron_description,'
                           ' mm_cron_enabled,'
                           ' mm_cron_schedule,'
                           ' mm_cron_last_run,'
                           ' mm_cron_json'
                           ' from mm_cron'
                           ' where mm_cron_guid = %s', (cron_uuid,))
    return self.db_cursor.fetchone()
