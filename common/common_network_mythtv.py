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
import MythTV

class CommonNetMythTV(object):
    """
    Class for interfacing with mythtv
    """
    def __init__(self, option_config_json):
        self.mythTV = MythTV.MythBE()

    def com_net_mythtv_programlist(self):
        self.programList = self.mythTV.getRecordings()

    def com_net_mythtv_delete_recording(self, program, forget):
        self.mythTV.deleteRecording(program, forget)

'''
str(program.title))
str(program.subtitle))
str(program.starttime))
'''
