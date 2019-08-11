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


def db_notification_insert(self, notification_data, notification_dismissable):
    """
    # insert notifications
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_notification (mm_notification_guid,'
                           'mm_notification_text,mm_notification_time,'
                           'mm_notification_dismissable)'
                           ' values (%s,%s,CURRENT_TIMESTAMP,%s)', (new_guid, notification_data,
                                                                    notification_dismissable))
    self.db_commit()
    return new_guid


def db_notification_read(self, offset=0, records=None):
    """
    # read all notifications
    """
    self.db_cursor.execute('select mm_notification_guid, mm_notification_text,'
                           ' mm_notification_time, mm_notification_dismissable'
                           ' from mm_notification'
                           ' order by mm_notification_time desc offset %s limit %s',
                           (offset, records))
    return self.db_cursor.fetchall()


def db_notification_delete(self, notification_uuid):
    """
    # remove notifications
    """
    self.db_cursor.execute('delete from mm_notification where mm_notification_guid = %s',
                           (notification_uuid,))
    self.db_commit()
