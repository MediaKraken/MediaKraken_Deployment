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
import logging # pylint: disable=W0611
import uuid


def srv_db_notification_insert(self, notification_data, notification_dismissable):
    """
    # insert notifications
    """
    self.db_cursor.execute('insert into mm_notification (mm_notification_guid,'\
        'mm_notification_text,mm_notification_time,mm_notification_dismissable)'\
        ' values (%s,%s,CURRENT_TIMESTAMP,%s)', (str(uuid.uuid4()), notification_data,\
        notification_dismissable))


def srv_db_notification_read(self, offset=None, records=None):
    """
    # read all notifications
    """
    if offset is None:
        self.db_cursor.execute('select mm_notification_guid, mm_notification_text,'\
            ' mm_notification_time, mm_notification_dismissable from mm_notification'\
            ' order by mm_notification_time desc')
    else:
        self.db_cursor.execute('select mm_notification_guid, mm_notification_text,'\
            ' mm_notification_time, mm_notification_dismissable from mm_notification'\
            ' order by mm_notification_time desc offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def srv_db_notification_delete(self, notification_uuid):
    """
    # remove noticications
    """
    self.db_cursor.execute('delete from mm_notification where mm_notification_guid = %s',\
        (notification_uuid,))
    self.db_cursor.commit()
