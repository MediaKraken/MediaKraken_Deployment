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
import datetime
import json

#class MK_Server_Database_Users:
# return user count
def MK_Server_Database_User_List_Name_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_user')
    return self.sql3_cursor.fetchone()[0]


# return user list
def MK_Server_Database_User_List_Name(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select id, username, email, created_at, active, is_admin, lang from mm_user order by LOWER(username)')
    else:
        self.sql3_cursor.execute('select id, username, email, created_at, active, is_admin, lang from mm_user where id in (select id from mm_user order by LOWER(username) offset %s limit %s) order by LOWER(username)', (offset, records))
    return self.sql3_cursor.fetchall()


# return all data for specified user
def MK_Server_Database_User_Detail(self, guid):
    self.sql3_cursor.execute('select * from mm_user where id = %s', (guid,))
    return self.sql3_cursor.fetchone()


# remove user
def MK_Server_Database_User_Delete(self, user_guid):
    self.sql3_cursor.execute('delete from mm_user where id = %s', (user_guid,))


# verify user logon
def MK_Server_Database_User_Login_Kodi(self, user_data):
    user_data = json.loads(user_data)
    self.sql3_cursor.execute('select id,password from mm_user where username = %s',\
        (user_data['username'],))
    result = self.sql3_cursor.fetchone()
    logging.debug("what: $s", result)
    if result is not None:
        if user_data['password'] == result['password'] or True: # pass matches   # TODO passowrd validation
            return (result[0], str(uuid.uuid4()))
        else:
            return (result[0], None)
    else:
        return (None, None)
