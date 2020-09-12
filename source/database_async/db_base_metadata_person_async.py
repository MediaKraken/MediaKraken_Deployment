import json
import uuid

from common import common_global


async def db_meta_person_as_seen_in(self, person_guid):
    """
    # find other media for person
    """
    row_data = await self.db_meta_person_by_guid(guid=person_guid)
    if row_data is None:  # exit on not found person
        return None
    # TODO jin index the credits
    common_global.es_inst.com_elastic_index('info', {"row_data": row_data})
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select mm_metadata_guid,mm_media_name,'
                                          ' mm_metadata_localimage_json->\'Poster\''
                                          ' from mm_metadata_movie'
                                          ' where mm_metadata_json->\'credits\'->\'cast\''
                                          ' @> \'[{"id": '
                                          + str(row_data['mmp_person_media_id'])
                                          + '}]\' order by LOWER(mm_media_name)) as json_data')


async def db_meta_person_by_guid(self, guid):
    """
    # return person data
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mmp_id, mmp_person_media_id,'
                                             ' mmp_person_meta_json,'
                                             ' mmp_person_image, mmp_person_name,'
                                             ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                             ' from mm_metadata_person where mmp_id = $1)'
                                             ' as json_data',
                                             guid)


async def db_meta_person_list(self, offset=0, records=None, search_value=None):
    """
    # return list of people
    """
    # TODO order by birth date
    if search_value is not None:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mmp_id,mmp_person_name,'
                                              ' mmp_person_image,'
                                              ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                              ' from mm_metadata_person where mmp_person_name % $1'
                                              ' order by LOWER(mmp_person_name) offset $2 limit $3)'
                                              ' as json_data',
                                              search_value, offset, records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mmp_id,mmp_person_name,'
                                              ' mmp_person_image,'
                                              ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                              ' from mm_metadata_person'
                                              ' order by LOWER(mmp_person_name)'
                                              ' offset $1 limit $2) as json_data',
                                              offset, records)


async def db_meta_person_list_count(self, search_value=None):
    """
    # count person metadata
    """
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_person'
                                                 ' where mmp_person_name % $1', search_value)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_person')


async def db_meta_person_id_count(self, guid):
    """
    # does person exist already by host/id
    """
    return await self.db_connection.fetchval('select count(*) from mm_metadata_person'
                                             ' where mmp_person_media_id = $1', guid)


async def db_meta_person_insert(self, person_name, media_id, person_json,
                                image_path=None):
    """
    # insert person
    """
    common_global.es_inst.com_elastic_index('info', {'db pers insert': {'name': person_name,
                                                                        'id': media_id,
                                                                        'person': person_json,
                                                                        'image': image_path}})
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_metadata_person (mmp_id, mmp_person_name,'
                                     ' mmp_person_media_id,'
                                     ' mmp_person_meta_json,'
                                     ' mmp_person_image)'
                                     ' values ($1,$2,$3,$4,$5)',
                                     new_guid, person_name, media_id,
                                     person_json, image_path)
    await self.db_connection.execute('commit')
    return new_guid


async def db_meta_person_insert_cast_crew(self, meta_type, person_json):
    """
    # batch insert from json of crew/cast
    """
    common_global.es_inst.com_elastic_index('info', {
        'db_meta_person_insert_cast_crew': meta_type, 'person': person_json})
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
            if meta_type == "themoviedb":
                person_id = person_data['id']
                person_name = person_data['name']
            else:
                person_id = None
                person_name = None
            if person_id is not None:
                # TODO do an upsert instead
                if await self.db_meta_person_id_count(person_id) > 0:
                    common_global.es_inst.com_elastic_index('info', {
                        'db_meta_person_insert_cast_crew': "skip insert as person exists"})
                else:
                    # Shouldn't need to verify fetch doesn't exist as the person insert
                    # is right below.  As then the next person record read will find
                    # the inserted record.
                    # insert download record for bio/info
                    await self.db_download_insert(meta_type, common_global.DLMediaType.Person.value,
                                                  json.dumps({"Status": "Fetch",
                                                              "ProviderMetaID": str(
                                                                  person_id)}))
                    # insert person record
                    await self.db_meta_person_insert(person_name,
                                                     person_id,
                                                     None, None)
    else:
        if meta_type == "themoviedb":
            # cast/crew can exist but be blank
            try:
                person_id = person_json['id']
                person_name = person_json['name']
            except:
                person_id = None
        else:
            person_id = None
            # person_name = None # not used later so don't set
        if person_id is not None:
            if await self.db_meta_person_id_count(meta_type, person_id) > 0:
                common_global.es_inst.com_elastic_index('info', {'stuff': "skippy"})
            else:
                # Shouldn't need to verify fetch doesn't exist as the person insert
                # is right below.  As then the next person record read will find
                # the inserted record.
                # insert download record for bio/info
                await self.db_download_insert(meta_type, common_global.DLMediaType.Person.value,
                                              json.dumps({"Status": "Fetch",
                                                          "ProviderMetaID": str(
                                                              person_id)}))
                # insert person record
                await self.db_meta_person_insert(person_name,
                                                 person_id,
                                                 None, None)
