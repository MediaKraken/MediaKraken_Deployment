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
import uuid
import psycopg2
import json
import time
import sys
sys.path.append("../../common")
from common import common_metadata_tmdb
sys.path.append("../../server")  # for db import
import database as database_base
# import localization
import locale
locale.setlocale(locale.LC_ALL, '')

# functions to deal with database data
sql3_conn = None
sql3_cursor = None

'''
"images/themoviedb/p/original";
"images/themoviedb/p/w45";
"images/themoviedb/p/w92";
"images/themoviedb/p/w130/";
"images/themoviedb/p/w154/";
"images/themoviedb/p/w185/";
"images/themoviedb/p/w780/";
backdrop_sizes": [
  "w300",
  "w780",
  "w1280",
  "original"
],
"logo_sizes": [
  "w45",
  "w92",
  "w154",
  "w185",
  "w300",
  "w500",
  "original"
],
"poster_sizes": [
  "w92",
  "w154",
  "w185",
  "w342",
  "w500",
  "w780",
  "original"
],
"profile_sizes": [
  "w45",
  "w185",
  "h632",
  "original"
],
"still_sizes": [
  "w92",
  "w185",
  "w300",
  "original"
]
'''

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../../MediaKraken_Server/MediaKraken.ini")


# verify themovietb key exists
if Config.get('API', 'themoviedb').strip() != 'None':
    # setup the thmdb class
    TMDB_API_CONNECTION = common_metadata_tmdb.CommonMetadataTMDB()
    print("Using key %s", Config.get('API', 'themoviedb').strip())
else:
    TMDB_API_CONNECTION = None
    print("API not available.")

# open the database
db = database_base.MKServerDatabase()
db.db_open(Config.get('DB Connections', 'PostDBHost').strip(),\
     Config.get('DB Connections', 'PostDBPort').strip(),\
     Config.get('DB Connections', 'PostDBName').strip(),\
     Config.get('DB Connections', 'PostDBUser').strip(),\
     Config.get('DB Connections', 'PostDBPass').strip())


total_movie_added = 0
if TMDB_API_CONNECTION is not None:
    # setup for unicode
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    sql3_conn = psycopg2.connect("dbname='metamandb' user='metamanpg'"\
        " host='localhost' password='metamanpg'")
    sql3_cursor = sql3_conn.cursor()
    # start up the range fetches
    for tmdb_to_fetch in range(364656, 500000):
    #for tmdb_to_fetch in range(353800, 500000):
        print("tmdb to fetch: %s", tmdb_to_fetch)
        # check to see if we already have it
        sql_params = str(tmdb_to_fetch),
        sql3_cursor.execute('select count(*) from mm_metadata_movie'\
            ' where mm_metadata_media_id->>\'tmdb\' = %s', sql_params)
        if sql3_cursor.fetchone()[0] > 0:
            print("found")
        else:
            print("adding")
            result_json = TMDB_API_CONNECTION.com_tmdb_Metadata_by_ID(tmdb_to_fetch)
            if result_json is not None:
                series_id_json, result_json, image_json\
                    = TMDB_API_CONNECTION.com_tmdb_metadata_info_build(result_json)
                cast_json = TMDB_API_CONNECTION.com_tmdb_metadata_cast_by_id(tmdb_to_fetch)
                # set and insert the record
                meta_json = ({'Meta': {'themoviedb': {'Meta': result_json, 'Cast': cast_json['cast'],\
                    'Crew': cast_json['crew']}}})
                sql_params = str(uuid.uuid4()), series_id_json, result_json['title'],\
                    json.dumps(meta_json), json.dumps(image_json)
                print("inserting record")
                sql3_cursor.execute('insert into mm_metadata_movie (mm_metadata_guid,'\
                    ' mm_metadata_media_id, mm_media_name, mm_metadata_json,'\
                    ' mm_metadata_localimage_json) values (%s,%s,%s,%s,%s)', sql_params)
                # store person info
                if 'cast' in cast_json:
                    db.db_meta_person_insert_cast_crew('themoviedb', cast_json['cast'])
                if 'crew' in cast_json:
                    db.db_meta_person_insert_cast_crew('themoviedb', cast_json['crew'])
                # grab reviews
                review_json = TMDB_API_CONNECTION.com_tmdb_metadata_review_by_id(tmdb_to_fetch)
                if review_json['total_results'] > 0:
                    review_json_id = ({'themoviedb': str(review_json['id'])})
                    print("rewview: %s", review_json_id)
                    sql_params = str(uuid.uuid4()), json.dumps(review_json_id),\
                        json.dumps({'themoviedb': review_json})
                    sql3_cursor.execute('insert into mm_review (mm_review_guid,'\
                        ' mm_review_metadata_id, mm_review_json) values (%s,%s,%s)', sql_params)
                sql3_conn.commit()
                # commit all changes
                db.db_commit()
                total_movie_added += 1
            time.sleep(2)
    # close the db
    sql3_conn.close()


# send notications
if total_movie_added > 0:
    db.db_notification_insert(locale.format('%d', total_movie_added, True)\
        + " Movie(s) metadata added.", True)


# commit all changes
db.db_commit()


# close DB
db.db_close()
