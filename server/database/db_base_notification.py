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


# insert notifications
def MK_Server_Database_Notification_Insert(self, notification_data, notification_dismissable):
    self.sql3_cursor.execute('insert into mm_notification (mm_notification_guid,mm_notification_text,mm_notification_time,mm_notification_dismissable) values (%s,%s,CURRENT_TIMESTAMP,%s)', (str(uuid.uuid4()), notification_data, notification_dismissable))


# read all notifications
def MK_Server_Database_Notification_Read(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable from mm_notification order by mm_notification_time desc')
    else:
        self.sql3_cursor.execute('select mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable from mm_notification order by mm_notification_time desc offset %s limit %s', (offset, records))
    return self.sql3_cursor.fetchall()


# remove noticications
def MK_Server_Database_Notification_Delete(self, notification_uuid):
    self.sql3_cursor.execute('delete from mm_notification where mm_notification_guid = %s', (notification_uuid,))
    self.sql3_cursor.commit()
