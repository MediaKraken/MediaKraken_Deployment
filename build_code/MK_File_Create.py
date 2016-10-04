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


# use this program to update from last alpha
from __future__ import absolute_import, division, print_function, unicode_literals
import sqlite3
import os


# connect/open lib db
sql3_emby_conn = sqlite3.connect('library.db')
sql3_emby_cursor = sql3_emby_conn.cursor()
sql3_emby_conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")

sql3_emby_cursor.execute('select Path from TypedBaseItems where Path is not null'\
    ' and type in ("MediaBrowser.Controller.Entities.Trailer",\
    "MediaBrowser.Controller.Entities.Movies.Movie",\
    "MediaBrowser.Controller.Entities.TV.Episode",\
    "MediaBrowser.Controller.Entities.Video")')

total_rows = 0
for row_data in sql3_emby_cursor.fetchall():
    total_rows += 1
    print('row: %s' % row_data[0])
print('Total: %s' % total_rows)


# select type, Path from TypedBaseItems group by type