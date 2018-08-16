'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import uuid


def db_task_insert(self, task_name, task_desc, task_enabled, task_schedule, task_last_run,
                   task_file_path, task_json):
    """
    insert task job
    """
    new_task_id = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_task (mm_task_guid, mm_task_name,'
                           ' mm_task_description, mm_task_enabled, mm_task_schedule,'
                           ' mm_task_last_run,'
                           ' mm_task_file_path, mm_task_json) values (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (new_task_id, task_name, task_desc, task_enabled, task_schedule,
                            task_last_run, task_file_path, task_json))
    return new_task_id


def db_task_list_count(self, enabled_only=False):
    """
    Return number of task jobs
    """
    if not enabled_only:
        self.db_cursor.execute('select count(*) from mm_task')
    else:
        self.db_cursor.execute(
            'select count(*) from mm_task where mm_task_enabled = true')
    return self.db_cursor.fetchone()[0]


def db_task_list(self, enabled_only=False, offset=None, records=None):
    """
    Return task list
    """
    if offset is None:
        if not enabled_only:
            self.db_cursor.execute('select mm_task_guid, mm_task_name, mm_task_description,'
                                   ' mm_task_enabled, mm_task_schedule, mm_task_last_run,'
                                   ' mm_task_file_path,'
                                   ' mm_task_json from mm_task order by mm_task_name')
        else:
            self.db_cursor.execute('select mm_task_guid, mm_task_name, mm_task_description,'
                                   ' mm_task_enabled, mm_task_schedule, mm_task_last_run,'
                                   ' mm_task_file_path, mm_task_json from mm_task'
                                   ' where mm_task_enabled = true order by mm_task_name')
    else:
        if not enabled_only:
            self.db_cursor.execute('select mm_task_guid, mm_task_name, mm_task_description,'
                                   ' mm_task_enabled, mm_task_schedule, mm_task_last_run,'
                                   ' mm_task_file_path, mm_task_json from mm_task'
                                   ' where mm_task_guid in (select mm_task_guid from mm_task'
                                   ' order by mm_task_name offset %s limit %s)'
                                   ' order by mm_task_name', (offset, records))
        else:
            self.db_cursor.execute('select mm_task_guid, mm_task_name, mm_task_description,'
                                   ' mm_task_enabled, mm_task_schedule, mm_task_last_run,'
                                   ' mm_task_file_path, mm_task_json'
                                   ' from mm_task where mm_task_guid '
                                   ' in (select mm_task_guid from mm_task'
                                   ' where mm_task_enabled = true order by mm_task_name'
                                   ' offset %s limit %s)'
                                   ' order by mm_task_name', (offset, records))
            return self.db_cursor.fetchall()


def db_task_time_update(self, task_type):
    """
    Update the datetime in which a task job was run
    """
    self.db_cursor.execute('update mm_task set mm_task_last_run = %s'
                           ' where mm_task_name = %s',
                           (datetime.datetime.now(), task_type))


def db_task_delete(self, task_uuid):
    """
    Delete task job
    """
    self.db_cursor.execute('delete from mm_task where mm_task_guid = %s',
                           (task_uuid,))


def db_task_info(self, task_uuid):
    """
    task job info
    """
    self.db_cursor.execute('select mm_task_guid, mm_task_name,'
                           ' mm_task_description, mm_task_enabled, mm_task_schedule,'
                           ' mm_task_last_run, mm_task_file_path, mm_task_json'
                           ' from mm_task where mm_task_guid = %s', (task_uuid,))
    return self.db_cursor.fetchone()
