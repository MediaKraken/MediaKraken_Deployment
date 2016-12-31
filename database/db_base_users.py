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
import json


#class ServerDatabaseUsers(object):
def db_user_list_name_count(self):
    """
    # return user count
    """
    self.db_cursor.execute('select count(*) from mm_user')
    return self.db_cursor.fetchone()[0]


def db_user_list_name(self, offset=None, records=None):
    """
    # return user list
    """
    if offset is None:
        self.db_cursor.execute('select id, username, email, created_at, active, is_admin, lang'\
            ' from mm_user order by LOWER(username)')
    else:
        self.db_cursor.execute('select id, username, email, created_at, active, is_admin, lang'\
            ' from mm_user where id in (select id from mm_user order by LOWER(username)'\
            ' offset %s limit %s) order by LOWER(username)', (offset, records))
    return self.db_cursor.fetchall()


def db_user_detail(self, guid):
    """
    # return all data for specified user
    """
    self.db_cursor.execute('select * from mm_user where id = %s', (guid,))
    return self.db_cursor.fetchone()


def db_user_delete(self, user_guid):
    """
    # remove user
    """
    self.db_cursor.execute('delete from mm_user where id = %s', (user_guid,))


def db_user_login_kodi(self, user_data):
    """
    # verify user logon
    """
    user_data = json.loads(user_data)
    self.db_cursor.execute('select id,password from mm_user where username = %s',\
        (user_data['username'],))
    result = self.db_cursor.fetchone()
    logging.info("what: %s", result)
    if result is not None:
        if user_data['password'] == result['password'] or True: # pass matches
            # TODO passowrd validation
            return (result[0], str(uuid.uuid4()))
        else:
            return (result[0], None)
    else:
        return (None, None)


def db_user_group_insert(self, group_name, group_desc, group_rights_json):
    """
    insert user group
    """
    self.db_cursor.execute('insert into mm_user_group (mm_user_group_guid,'\
        ' mm_user_group_name, mm_user_group_description, mm_user_group_rights_json)'\
        ' values (%s,%s,%s,%s)', (str(uuid.uuid4()), group_name, group_desc, group_rights_json))


def db_user_profile_insert(self, profile_name, profile_json):
    """
    insert user profile
    """
    self.db_cursor.execute('insert into mm_user_profile (mm_user_profile_guid,'\
        ' mm_user_profile_name, mm_user_profile_json) values (%s, %s, %s)', \
        (str(uuid.uuid4()), profile_name, profile_json))
