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
import logging
import uuid
import json


# count person metadata
def MK_Server_Database_Metadata_Person_List_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_metadata_person')
    return self.sql3_cursor.fetchone()[0]


# return list of people
def MK_Server_Database_Metadata_Person_List(self, offset=None, records=None):
    if offset is None:
        self.sql3_cursor.execute('select mmp_id,mmp_person_name, mmp_person_image from mm_metadata_person order by mmp_person_name')
    else:
        self.sql3_cursor.execute('select mmp_id,mmp_person_name,mmp_person_image from mm_metadata_person where mmp_id in (select mmp_id from mm_metadata_person order by mmp_person_name offset %s limit %s) order by mmp_person_name', (offset, records))
    return self.sql3_cursor.fetchall()


# return person data
def MK_Server_Database_Metadata_Person_By_GUID(self, guid):
    self.sql3_cursor.execute('select mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name from mm_metadata_person where mmp_id = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# return person data by name
def MK_Server_Database_Metadata_Person_By_Name(self, person_name):
    self.sql3_cursor.execute('select mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name from mm_metadata_person where mmp_person_name = %s', (person_name,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# does person exist already by host/id
def MK_Server_Database_Metadata_Person_ID_Count(self, host_type, guid):
    #sql_params = host_type, guid
    #self.sql3_cursor.execute('select count(*) from mm_metadata_person where mmp_person_media_id @> \'{"Host":%s}\' and mmp_person_meta_json @> \'{"id":%s}\'', sql_params)
    self.sql3_cursor.execute('select count(*) from mm_metadata_person where mmp_person_media_id @> \'{"Host":"' + host_type + '"}\' and mmp_person_media_id @> \'{"id":%s}\'', (guid,))
    return self.sql3_cursor.fetchone()[0]
# works in postgresql
# select count(*) from mm_metadata_person where mmp_person_media_id @> '{"Host":"TMDB"}' and mmp_person_meta_json @> '{"id":169}'


# insert person
def MK_Server_Database_Metdata_Person_Insert(self, person_name, media_id_json, person_json,\
        image_json=None):
    self.sql3_cursor.execute('insert into mm_metadata_person (mmp_id, mmp_person_name, mmp_person_media_id, mmp_person_meta_json, mmp_person_image) values (%s,%s,%s,%s,%s)', (str(uuid.uuid4()), person_name, media_id_json, person_json, image_json))


# batch insert from json of crew/cast
def MK_Server_Database_Metadata_Person_Insert_Cast_Crew(self, meta_type, person_json):
    # TODO failing due to only one person in json?  hence pulling id, etc as the for loop
    try:
        for person_data in person_json:
            #logging.debug("person data: %s", person_data)
    #        person_data = json.dumps(person_data)
            if meta_type == "TVMaze":
                person_id = person_data['person']['id']
                person_name = person_data['person']['name']
            elif meta_type == "TMDB":
                person_id = person_data['id']
                person_name = person_data['name']
            elif meta_type == "theTVDB":
                person_id = int(person_data['id'])
                person_name = person_data['Name']
            else:
                person_id = None
                person_name = None
            if person_id is not None:
                if self.MK_Server_Database_Metadata_Person_ID_Count(meta_type, person_id) > 0:
                    logging.debug("skippy")
                else:
                    self.MK_Server_Database_Metdata_Person_Insert(person_name,\
                        json.dumps({'Host': meta_type, 'id': person_id}), None,\
                        json.dumps({'ImageFetch': True})) #, 'Prof': person_data['profile_path']}))       
    except:
        if meta_type == "TVMaze":
            person_id = person_json['person']['id']
            person_name = person_json['person']['name']
        elif meta_type == "TMDB":
            person_id = person_json['id']
            person_name = person_json['name']
        elif meta_type == "theTVDB":
            person_id = int(person_json['id'])
            person_name = person_json['Name']
        else:
            person_id = None
            person_name = None
        if person_id is not None:
            if self.MK_Server_Database_Metadata_Person_ID_Count(meta_type, person_id) > 0:
                logging.debug("skippy")
            else:
                self.MK_Server_Database_Metdata_Person_Insert(person_name,\
                    json.dumps({'Host': meta_type, 'id': person_id}), None,\
                    json.dumps({'ImageFetch': True})) #, 'Prof': person_data['profile_path']}))


# find other media for person
def MK_Server_Database_Metadata_Person_As_Seen_In(self, person_guid):
    row_data = self.MK_Server_Database_Metadata_Person_By_GUID(person_guid)
    logging.debug("row_data: %s", row_data[1])
    if row_data['mmp_person_media_id']['Host'] == 'TMDB':
        sql_params = row_data['mmp_person_media_id']['id'],
        self.sql3_cursor.execute('select mm_metadata_guid,mm_media_name,mm_metadata_localimage_json->\'Images\'->\'TMDB\'->\'Poster\' from mm_metadata_movie where mm_metadata_json->\'Meta\'->\'TMDB\'->\'Cast\' @> \'[{"id":%s}]\'', sql_params)
    elif row_data['mmp_person_media_id']['Host'] == 'TVMaze':
        sql_params = row_data['mmp_person_media_id']['id'],
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,mm_metadata_tvshow_localimage_json->\'Images\'->\'TVMaze\'->\'Poster\' from mm_metadata_tvshow WHERE mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'cast\' @> \'[{"person": {"id": %s}}]\'', sql_params)  # TODO won't this need to be like below?
    elif row_data['mmp_person_media_id']['Host'] == 'theTVDB':
        #sql_params = str(row_data[1]['id']),
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,mm_metadata_tvshow_localimage_json->\'Images\'->\'theTVDB\'->\'Poster\' from mm_metadata_tvshow where mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Cast\'->\'Actor\' @> \'[{"id": \"' + str(row_data['mmp_person_media_id']['id']) + '\"}]\'')  #, sql_params)  #TODO
    return self.sql3_cursor.fetchall()

## works
#select mm_metadata_tvshow_guid,mm_metadata_tvshow_name as media_query_name,mm_metadata_tvshow_localimage_json
#from mm_metadata_tvshow WHERE mm_metadata_tvshow_json->'Meta'->'TVMaze'->'_embedded'->'cast' @> '[{"person": {"id": 96405}}]'
