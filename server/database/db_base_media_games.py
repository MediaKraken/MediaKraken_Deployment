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


def com_media_game_system_list_count(self):
    """
    Audited system list count
    """
    pass


def com_media_game_system_list(self, offset=None, records=None):
    """
    Audited system list
    """
    pass


def com_media_game_list_by_system_count(self, system_id):
    """
    Audited game list by system count
    """
    pass


def com_media_game_list_by_system(self, system_id, offset=None, records=None):
    """
    Audited game list by system
    """
    pass


def com_media_game_list_count(self):
    """
    Audited games list count
    """
    pass


def com_media_game_list(self, offset=None, records=None):
    """
    Audited games list
    """
    pass
