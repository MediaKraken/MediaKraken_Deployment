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
import psycopg2


class MK_Server_Database_Brainz:
    def __init__(self):
        self.sql3_conn = None
        self.sql3_cursor = None


    # open database and pull in config from sqlite and create db if not exist
    def MK_Server_Database_Open(self, PostDBHost, PostDBPort, PostDBName, PostDBUser, PostDBPass):
        # setup for unicode
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
        #psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
        #psycopg2.extras.register_default_json(loads=lambda x: x)
        self.sql3_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'"\
            % (PostDBName, PostDBUser, PostDBHost, int(PostDBPort), PostDBPass))
        self.sql3_cursor = self.sql3_conn.cursor()
        self.sql3_cursor.execute("SET TIMEZONE = 'America/Chicago'")
#        self.sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class WHERE relname = 'mm_media'")
#        if self.sql3_cursor.fetchone()[0] == 0:
#            exit(1)


    # close main db file
    def MK_Server_Database_Close(self):
        self.sql3_conn.close()


    # read in all artists
    def MK_Server_Database_Brainz_All_Artists(self):
        self.sql3_cursor.execute('select gid,name,sort_name,comment,begin_date_year,begin_date_month,begin_date_day,end_date_year,end_date_month,end_date_day,gender,id from artist')
        return self.sql3_cursor.fetchall()

    # read in all albums
    def MK_Server_Database_Brainz_All_Albums(self):
        self.sql3_cursor.execute('select gid,name,artist_credit,comment,language,barcode,id from release')
        return self.sql3_cursor.fetchall()


    # read in album by artist credit id
    def MK_Server_Database_Brainz_All_Albums_By_Artist(self, artist_id):
        self.sql3_cursor.execute('select gid,name,artist_credit,comment,language,barcode,id from release where artist_credit = %s', (artist_id,))
        return self.sql3_cursor.fetchall()


    # read in all songs
    def MK_Server_Database_Brainz_All_Songs(self):
        self.sql3_cursor.execute('select gid,name,recording,position,id from track')
        return self.sql3_cursor.fetchall()


    # read in all by recording id
    def MK_Server_Database_Brainz_All_Songs_By_Record_UUID(self, record_id):
        self.sql3_cursor.execute('select gid,name,recording,position,id from track where recording = %s', (record_id,))
        return self.sql3_cursor.fetchall()


    # read for batch insert
    def MK_Server_Database_Brainz_All(self):
        self.sql3_cursor.execute('select count(*) from artist, release, track where release.artist_credit = artist.id and track.recording = release.id')
        return self.sql3_cursor.fetchall()
