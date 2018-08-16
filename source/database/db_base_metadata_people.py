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

import json
import uuid

from common import common_global


def db_meta_person_list_count(self, search_value=None):
    """
    # count person metadata
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_person'
                               ' where mmp_person_name %% %s', (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_person')
    return self.db_cursor.fetchone()[0]


def db_meta_person_list(self, offset=None, records=None, search_value=None):
    """
    # return list of people
    """
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select mmp_id,mmp_person_name,mmp_person_image,'
                                   'mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                   ' from mm_metadata_person where mmp_person_name %% %s'
                                   ' order by mmp_person_name', (search_value,))
        else:
            self.db_cursor.execute('select mmp_id,mmp_person_name,mmp_person_image,'
                                   'mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                   ' from mm_metadata_person order by mmp_person_name')
    else:
        if search_value is not None:
            self.db_cursor.execute('select mmp_id,mmp_person_name,mmp_person_image,'
                                   'mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                   ' from mm_metadata_person where mmp_person_name %% %s'
                                   ' order by mmp_person_name offset %s limit %s',
                                   (search_value, offset, records))
        else:
            self.db_cursor.execute('select mmp_id,mmp_person_name,mmp_person_image,'
                                   'mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                   ' from mm_metadata_person order by mmp_person_name'
                                   ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_person_by_guid(self, guid):
    """
    # return person data
    """
    self.db_cursor.execute('select mmp_id, mmp_person_media_id, mmp_person_meta_json,'
                           ' mmp_person_image, mmp_person_name from mm_metadata_person'
                           ' where mmp_id = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_person_by_name(self, person_name):
    """
    # return person data by name
    """
    self.db_cursor.execute('select mmp_id, mmp_person_media_id, mmp_person_meta_json,'
                           ' mmp_person_image, mmp_person_name from mm_metadata_person'
                           ' where mmp_person_name = %s', (person_name,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_person_id_count(self, host_type, guid):
    """
    # does person exist already by host/id
    """
    self.db_cursor.execute('select count(*) from mm_metadata_person'
                           ' where mmp_person_media_id @> \'{"' +
                           host_type + '":"'
                           + str(guid) + '"}\'')
    return self.db_cursor.fetchone()[0]


# works after the refactor
# select count(*) from mm_metadata_person where mmp_person_media_id @> '{"themoviedb": "22358"}'
# works in postgresql
# select count(*) from mm_metadata_person where mmp_person_media_id @> '{"Host":"themoviedb"}'
# and mmp_person_meta_json @> '{"id":169}'


def db_meta_person_insert(self, person_name, media_id_json, person_json,
                          image_json=None):
    """
    # insert person
    """
    common_global.es_inst.com_elastic_index('info', {'db pers insert': {'name': person_name,
                                                                        'id': media_id_json,
                                                                        'person': person_json,
                                                                        'image': image_json}})
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_person (mmp_id, mmp_person_name,'
                           ' mmp_person_media_id, mmp_person_meta_json, mmp_person_image)'
                           ' values (%s,%s,%s,%s,%s)', (new_guid, person_name, media_id_json,
                                                        person_json, image_json))
    self.db_commit()
    return new_guid


def db_meta_person_update(self, provider_name, provider_uuid, person_bio, person_image):
    """
    update the person bio/etc
    """
    self.db_cursor.execute('update mm_metadata_person set mmp_person_meta_json = %s, '
                           'mmp_person_image = %s where mmp_person_media_id->\''
                           + provider_name + '\' ? %s',
                           (json.dumps(person_bio), json.dumps(person_image),
                            str(provider_uuid)))
    self.db_commit()


def db_meta_person_insert_cast_crew(self, meta_type, person_json):
    """
    # batch insert from json of crew/cast
    """
    common_global.es_inst.com_elastic_index('info', {
        'db person insert cast crew': meta_type, 'person': person_json})
    # TODO failing due to only one person in json?  hence pulling id, etc as the for loop
    multiple_person = False
    try:
        for person_data in person_json:
            multiple_person = True
    except:
        pass
    if multiple_person:
        for person_data in person_json:
            common_global.es_inst.com_elastic_index('info', {"person data": person_data})
            if meta_type == "tvmaze":
                person_id = person_data['person']['id']
                person_name = person_data['person']['name']
            elif meta_type == "themoviedb":
                person_id = person_data['id']
                person_name = person_data['name']
            elif meta_type == "thetvdb":
                # handle "array" with only one person
                try:
                    person_id = person_data['id']
                    person_name = person_data['Name']
                except:
                    person_id = person_json['id']
                    person_name = person_json['Name']
            else:
                person_id = None
                person_name = None
            if person_id is not None:
                if self.db_meta_person_id_count(meta_type, person_id) > 0:
                    common_global.es_inst.com_elastic_index('info', {'stuff': "skippy"})
                else:
                    # insert download record for bio/info
                    self.db_download_insert(meta_type, 3, json.dumps({"Status": "Fetch",
                                                                      "ProviderMetaID": str(
                                                                          person_id)}))
                    # insert person record
                    self.db_meta_person_insert(person_name,
                                               json.dumps(
                                                   {meta_type: str(person_id)}),
                                               None, None)
    else:
        if meta_type == "tvmaze":
            person_id = person_json['person']['id']
            person_name = person_json['person']['name']
        elif meta_type == "themoviedb":
            # cast/crew can exist but be blank
            try:
                person_id = person_json['id']
                person_name = person_json['name']
            except:
                person_id = None
        elif meta_type == "thetvdb":
            person_id = person_json['id']
            person_name = person_json['Name']
        else:
            person_id = None
            # person_name = None # not used later so don't set
        if person_id is not None:
            if self.db_meta_person_id_count(meta_type, person_id) > 0:
                common_global.es_inst.com_elastic_index('info', {'stuff': "skippy"})
            else:
                # insert download record for bio/info
                self.db_download_insert(meta_type, 3, json.dumps({"Status": "Fetch",
                                                                  "ProviderMetaID": str(
                                                                      person_id)}))
                # insert person record
                self.db_meta_person_insert(person_name,
                                           json.dumps(
                                               {meta_type: str(person_id)}),
                                           None, None)


def db_meta_person_as_seen_in(self, person_guid):
    """
    # find other media for person
    """
    row_data = self.db_meta_person_by_guid(person_guid)
    if row_data is None:  # exit on not found person
        return None
    # TODO jin index the credits
    common_global.es_inst.com_elastic_index('info', {"row_data": row_data})
    if 'themoviedb' in row_data['mmp_person_media_id']:
        sql_params = int(row_data['mmp_person_media_id']['themoviedb']),
        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,'
                               'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\''
                               ' from mm_metadata_movie where mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'credits\'->\'cast\''
                               ' @> \'[{"id": %s}]\' order by mm_media_name', sql_params)
    elif 'tvmaze' in row_data['mmp_person_media_id']:
        sql_params = int(row_data['mmp_person_media_id']['tvmaze']),
        common_global.es_inst.com_elastic_index('info', {'sql paramts': sql_params})
        self.db_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                               'mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->\'Poster\''
                               ' from mm_metadata_tvshow WHERE mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
                               '->\'_embedded\'->\'cast\' @> \'[{"person": {"id": %s}}]\' order by mm_metadata_tvshow_name',
                               sql_params)
        # TODO won't this need to be like below?
    elif 'thetvdb' in row_data['mmp_person_media_id']:
        # sql_params = str(row_data[1]['thetvdb']),
        self.db_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                               'mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->\'Poster\''
                               ' from mm_metadata_tvshow where mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
                               '->\'Cast\'->\'Actor\' @> \'[{"id": \"'
                               + str(row_data['mmp_person_media_id']['thetvdb'])
                               + '\"}]\' order by mm_metadata_tvshow_name')  # , sql_params)  #TODO
    return self.db_cursor.fetchall()

# works
# select mm_metadata_tvshow_guid,mm_metadata_tvshow_name as
# media_query_name,mm_metadata_tvshow_localimage_json
# from mm_metadata_tvshow WHERE mm_metadata_tvshow_json->'Meta'
# ->'tvmaze'->'_embedded'->'cast' @> '[{"person": {"id": 96405}}]'
