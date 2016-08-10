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

import uuid
import logging


# return count of sync jobs
def MK_Server_Database_Link_List_Count(self):
    self.sql3_cursor.execute(u'select count(*) from mm_link')
    return self.sql3_cursor.fetchone()[0]


# return list of sync jobs
def MK_Server_Database_Link_List(self, offset=None, records=None):
    # complete list for admins
    if offset is None:
        self.sql3_cursor.execute(u'select mm_link_guid, mm_link_name, mm_link_json from mm_link')
    else:
        self.sql3_cursor.execute(u'select mm_link_guid, mm_link_name, mm_link_json from mm_link where mm_link_guid in (select mm_link_guid from mm_link offset %s limit %s)', (offset, records))
    return self.sql3_cursor.fetchall()


# insert sync job
def MK_Server_Database_Link_Insert(self, link_json):
    self.sql3_cursor.execute(u'insert into mm_link (mm_link_guid, mm_link_options_json) values (%s, %s)', (str(uuid.uuid4()), link_json))


# delete sync job
def MK_Server_Database_Link_Delete(self, sync_guid):
    self.sql3_cursor.execute(u'delete from mm_link where mm_link_guid = %s', (sync_guid,))
