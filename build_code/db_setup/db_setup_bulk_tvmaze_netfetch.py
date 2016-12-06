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
import uuid
import psycopg2
import json
import time
import sys
sys.path.append("../../common")
from common import common_metadata_tvmaze
sys.path.append("../../server")  # for db import
import database as database_base

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("../../MediaKraken.ini")

import locale
locale.setlocale(locale.LC_ALL, '')

tvmaze = common_metadata_tvmaze.com_meta_tvmaze_API()


# open the database
db = database_base.MKServerDatabase()
db.db_open(Config.get('DB Connections', 'PostDBHost').strip(),\
     Config.get('DB Connections', 'PostDBPort').strip(),\
     Config.get('DB Connections', 'PostDBName').strip(),\
     Config.get('DB Connections', 'PostDBUser').strip(),\
     Config.get('DB Connections', 'PostDBPass').strip())


total_show_added = 0
# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
sql3_conn = psycopg2.connect("dbname='metamandb' user='metamanpg'"\
    " host='localhost' password='metamanpg'")
sql3_cursor = sql3_conn.cursor()
sql3_cursor.execute("SELECT COUNT (relname) as a FROM pg_class WHERE relname = 'mm_media'")
if sql3_cursor.fetchone()[0] > 0:
    for page_ndx in range(63, 75):
        print(page_ndx)
        result = tvmaze.com_meta_tvmaze_show_list(page_ndx)
        show_list_json = json.loads(result)
        for show_ndx in range(0, len(show_list_json)):
            tvmaze_id = show_list_json[show_ndx]['id']
            print("id: %s", tvmaze_id)
            # check to see if allready downloaded
            sql_args = str(tvmaze_id),
            sql3_cursor.execute('SELECT COUNT(*) from mm_metadata_tvshow'\
                ' where mm_metadata_media_tvshow_id->\'tvmaze\' ? %s', sql_args)
            if sql3_cursor.fetchone()[0] > 0:
                print("skip id: %s", str(tvmaze_id))
            else:
                tvmaze_name = show_list_json[show_ndx]['name']
                print("fetch name: %s", tvmaze_name)
                show_full_json = ({'Meta': {'tvmaze':\
                    json.loads(tvmaze.com_meta_themaze_show_by_id(tvmaze_id, None, None,\
                    None, True))}})
                print("full: %s", show_full_json)
                if show_full_json is not None:
                    # populate other ids for lookup json
                    try:
                        tvrage_id = str(show_full_json['externals']['tvrage'])
                    except:
                        tvrage_id = None
                    try:
                        thetvdb_id = str(show_full_json['externals']['thetvdb'])
                    except:
                        thetvdb_id = None
                    try:
                        imdb_id = str(show_full_json['externals']['imdb'])
                    except:
                        imdb_id = None
                    series_id_json = json.dumps({'tvmaze':str(tvmaze_id), 'tvrage':tvrage_id,\
                        'imdb':imdb_id, 'thetvdb':thetvdb_id})
                    image_json = {'Images': {'tvmaze': {'Characters': {}, 'Episodes': {},\
                        "Redo": True}}}
                    sql_params = str(uuid.uuid4()), series_id_json, tvmaze_name,\
                        json.dumps(show_full_json), json.dumps(image_json)
                    sql3_cursor.execute('insert into mm_metadata_tvshow'\
                        ' (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id,'\
                        ' mm_metadata_tvshow_name, mm_metadata_tvshow_json,'\
                        ' mm_metadata_tvshow_localimage_json) values (%s,%s,%s,%s,%s)', sql_params)
                    print("inserted name")
                    sql3_conn.commit()
                    # store person info
                    if 'cast' in show_full_json['Meta']['tvmaze']['_embedded']:
                        db.db_meta_person_insert_cast_crew('tvmaze',\
                            show_full_json['Meta']['tvmaze']['_embedded']['cast'])
                    if 'crew' in show_full_json['Meta']['tvmaze']['_embedded']:
                        db.db_meta_person_insert_cast_crew('tvmaze',\
                            show_full_json['Meta']['tvmaze']['_embedded']['crew'])
                    # commit all changes
                    db.db_commit()
                    total_show_added += 1
                time.sleep(2)

# send notification
if total_show_added > 0:
    db.db_notification_insert(locale.format('%d', total_show_added, True)\
        + " TV show(s) metadata added.", True)


# commit and close
sql3_conn.commit()
sql3_conn.close()

# commit all changes
db.db_commit()


# close the database
db.db_close()
