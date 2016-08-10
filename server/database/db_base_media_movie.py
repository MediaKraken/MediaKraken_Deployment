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

import datetime
import logging

# TODO subselect speed

# find random movie
def MK_Server_Database_Media_Random(self, return_image_type=False):
    if not return_image_type:
        self.sql3_cursor.execute(u'select mm_metadata_guid,mm_media_guid from mm_media,mm_metadata_movie where mm_media_metadata_guid = mm_metadata_guid and random() < 0.01 limit 1')
    else:
        self.sql3_cursor.execute(u'select mm_metadata_localimage_json->\'LocalImages\'->>' + return_image_type + ',mm_media_guid from mm_media,mm_metadata where mm_media_metadata_guid = mm_metadata_guid and mm_metadata_localimage_json->\'LocalImages\'->>' + return_image_type + ' > \'\' and random() < 0.01 limit 1')
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# movie count by genre
def MK_Server_Database_Media_Movie_Count_By_Genre(self, class_guid):
    self.sql3_cursor.execute(u'select jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb as gen, count(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\') from ((select distinct on (mm_media_metadata_guid) mm_metadata_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid) union (select distinct on (mmr_media_metadata_guid) mm_metadata_json from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid)) as temp group by gen', (class_guid, class_guid))
    return self.sql3_cursor.fetchall()


# web media count
def MK_Server_Database_Web_Media_List_Count(self, class_guid, list_type=None, list_genre='All', group_collection=False, include_remote=False):
    logging.debug("classuid: %s %s", class_guid, list_type)
    #messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select count(*) from (select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s) as temp", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"),))
                else:
                    self.sql3_cursor.execute(u"select count(*) from ((select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s) union (select distinct mmr_metadata_guid from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mm_media_json->>'\DateAdded\' >= %s)) as temp", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")))
            else:
                pass
        else:
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select count(*) from (select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid) as temp", (class_guid,))
                else:
                    self.sql3_cursor.execute(u"select count(*) from ((select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid) union (select distinct mm_metadata_guid from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid)) as temp", (class_guid, class_guid))
            else:
                if not include_remote:
                    self.sql3_cursor.execute(u"select count(*) as row_count from ((select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and (mm_metadata_json->>'belongs_to_collection') is null) union (select count(*) from xxxx as row_count)) as temp", (class_guid, class_guid))
                else:
                    pass
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select count(*) from (select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s) as temp", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), list_genre))
                else:
                    self.sql3_cursor.execute(u"select count(*) from ((select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s) union (select distinct mmr_metadata_guid from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mmr_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s)) as temp", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), list_genre, class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), list_genre))
            else:
                pass
        else:
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select count(*) from (select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s) as temp", (class_guid, list_genre))
                else:
                    self.sql3_cursor.execute(u"select count(*) from ((select distinct mm_metadata_guid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s) union (select distinct mmr_media_metadata_guid from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s)) as temp", (class_guid, list_genre, class_guid, list_genre))
            else:
                pass
    return self.sql3_cursor.fetchone()[0]


# web media return
def MK_Server_Database_Web_Media_List(self, class_guid, list_type=None, list_genre='All', list_limit=0, group_collection=False, offset=0, include_remote=False):
    logging.debug("classuid: %s %s %s", class_guid, list_type, list_genre)
    #messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select * from (select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s order by mm_media_metadata_guid, mm_media_name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), offset, list_limit))
                else:
                    self.sql3_cursor.execute(u"select * from ((select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s order by mm_media_metadata_guid, mm_media_name) union (select distinct on (mmr_media_metadata_guid) mm_media_name, mmr_media_guid, mmr_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mmr_media_json->>\'DateAdded\' >= %s order by mmr_media_metadata_guid, mm_media_name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), offset, list_limit))
            else:
                pass
        else:
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select * from (select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid order by mm_media_metadata_guid, mm_media_name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, offset, list_limit))
                else:
                    self.sql3_cursor.execute(u"select * from ((select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid order by mm_media_metadata_guid, mm_media_name) union (select distinct on (mmr_media_metadata_guid) mm_media_name, mmr_media_guid, mmr_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid order by mmr_media_metadata_guid, mm_media_name)) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, class_guid, offset, list_limit))
            else:
                if not include_remote:
                    self.sql3_cursor.execute(u"select * from (select distinct on (mm_media_metadata_guid) mm_media_name as name, mm_media_guid as guid, mm_media_json as mediajson, mm_metadata_json, mm_metadata_localimage_json as metajson as metaguid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and (mm_metadata_json->>'belongs_to_collection') is null union select mm_metadata_collection_name as name, mm_metadata_collection_guid as guid, null as metaguid from xxxx order by mm_media_metadata_guid, name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, offset, list_limit))
                else:
                    self.sql3_cursor.execute(u"select * from ((select distinct on (mm_media_metadata_guid) mm_media_name as name, mm_media_guid as guid, mm_media_json as mediajson, mm_metadata_json, mm_metadata_localimage_json as metajson as metaguid from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and (mm_metadata_json->>'belongs_to_collection') is null) union (select mm_metadata_collection_name as name, mm_metadata_collection_guid as guid, null as metaguid from xxxx order by mm_media_metadata_guid, name) as temp order by LOWER(mm_media_name)) offset %s limit %s", (class_guid, class_guid, offset, list_limit))
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select * from (select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mm_media_metadata_guid, mm_media_name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), list_genre, offset, list_limit))
                else:
                    self.sql3_cursor.execute(u"select * from ((select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mm_media_metadata_guid, mm_media_name) union (select distinct on (mmr_media_metadata_guid) mm_media_name, mmr_media_guid, mmr_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mmr_media_json->>\'DateAdded\' >= %s and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mmr_media_metadata_guid, mm_media_name)) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), list_genre, offset, list_limit))
            else:
                pass
        else:
            if not group_collection:
                if not include_remote:
                    self.sql3_cursor.execute(u"select * from (select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mm_media_metadata_guid, mm_media_name) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, list_genre, offset, list_limit))
                else:
                    self.sql3_cursor.execute(u"select * from ((select distinct on (mm_media_metadata_guid) mm_media_name, mm_media_guid, mm_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media, mm_metadata_movie where mm_media_class_guid = %s and mm_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mm_media_metadata_guid, mm_media_name) union (select distinct on (mmr_media_metadata_guid) mm_media_name, mmr_media_guid, mmr_media_json, mm_metadata_json, mm_metadata_localimage_json from mm_media_remote, mm_metadata_movie where mmr_media_class_guid = %s and mmr_media_metadata_guid = mm_metadata_guid and mm_metadata_json->\'genres\'->0->\'name\' ? %s order by mmr_media_metadata_guid, mm_media_name)) as temp order by LOWER(mm_media_name) offset %s limit %s", (class_guid, list_genre, class_guid, list_genre, offset, list_limit))
            else:
                pass
    return self.sql3_cursor.fetchall()
