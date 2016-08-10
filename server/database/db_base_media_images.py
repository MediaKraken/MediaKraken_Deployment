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

import logging


# images list count
def MK_Common_Media_Images_List_Count(self):
    pass


# images list
def MK_Common_Media_Images_List(self, offset=None, records=None):
    self.sql3_cursor.execute(u'select mm_media_path from mm_media,mm_media_class where mm_media.mm_media_class_guid = mm_media_class.mm_media_class_guid and mm_media_class_type = \'Picture\'')
    return self.sql3_cursor.fetchall()
