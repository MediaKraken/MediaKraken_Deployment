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
import pytest
import sys
sys.path.append('.')
from common import common_watchdog


# class MK_Watchdog_Handler(FileSystemEventHandler):
#     def on_modified(self, event):


#     def on_deleted(self, event):


#     def on_moved(self, event):


#     def on_created(self, event):


#    def on_any_event(self, event):
#        logging.info("Any!", event.src_path)
#        pass


# define watchdog class
# class com_Watchdog_API:
#     def com_Watchdog_Start(self, paths_to_watch):


# stop watchdog
#    def com_Watchdog_Stop(self):
