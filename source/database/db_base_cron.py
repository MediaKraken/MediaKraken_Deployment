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
