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
import logging


# audited system list count
def MK_Common_Media_Game_System_List_Count(self):
    pass


# audited system list
def MK_Common_Media_Game_System_List(self, offset=None, records=None):
    pass


# audited game list by system count
def MK_Common_Media_Game_List_By_System_Count(self, system_id):
    pass


# audited game list by system
def MK_Common_Media_Game_List_By_System(self, system_id, offset=None, records=None):
    pass


# audited games list count
def MK_Common_Media_Game_List_Count(self):
    pass


# audited games list
def MK_Common_Media_Game_List(self, offset=None, records=None):
    pass
