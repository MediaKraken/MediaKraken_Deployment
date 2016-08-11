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


# insert channel
def MK_Server_Database_Channel_Insert(self, channel_id, channel_name, channel_language, channel_country, channel_logo_id):
    self.sql3_cursor.execute('select count(*) from blah where blah = %s', (channel_id,))
    if self.sql3_cursor.fetchall()[0] == 0:
        self.sql3_cursor.execute('')
