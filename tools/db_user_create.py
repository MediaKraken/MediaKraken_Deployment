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


import sqlite3
conn = sqlite3.connect('user.db')


con_cursor = conn.cursor()
# Create table
con_cursor.execute('''CREATE TABLE log_user (username text, email text, password text, is_admin integer)''')
# Insert a row of data
con_cursor.execute("INSERT INTO log_user VALUES ('SpootDev', 'spootdev@gmail.com', 'fakepass', 1)")
# Save (commit) the changes
conn.commit()
# close db
conn.close()
