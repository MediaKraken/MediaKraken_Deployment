'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import datetime


def srv_db_activity_insert(self, activity_name, activity_overview,\
        activity_short_overview, activity_type, activity_itemid, activity_userid,\
        activity_log_severity):
    """
    Insert server or user activity record
    """
    self.db_cursor.execute('insert into mm_user_activity (mm_activity_guid, mm_activity_name,'\
        ' mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid,'\
        ' mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity)'\
        ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (str(uuid.uuid4()), activity_name,\
        activity_overview, activity_short_overview, activity_type, activity_itemid,\
        activity_userid, datetime.datetime.now(), activity_log_severity))
    self.srv_db_commit()


def srv_db_activity_purge(self, days_old):
    """
    Purge records older than specified days
    """
    self.db_cursor.execute('delete from mm_user_activity where mm_activity_datecreated'\
        ' < now() - interval %s;', (str(days_old) + ' day',))
    self.srv_db_commit()
