from common import common_global


async def db_meta_person_as_seen_in(self, db_connection, person_guid):
    """
    # find other media for person
    """
    row_data = await self.db_meta_person_by_guid(db_connection=db_connection, guid=person_guid)
    if row_data is None:  # exit on not found person
        return None
    # TODO jin index the credits
    common_global.es_inst.com_elastic_index('info', {"row_data": row_data})
    return await db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                     'mm_metadata_localimage_json->\'Poster\''
                                     ' from mm_metadata_movie'
                                     ' where mm_metadata_json->\'credits\'->\'cast\''
                                     ' @> \'[{"id": '
                                     + str(row_data['mmp_person_media_id'])
                                     + '}]\' order by LOWER(mm_media_name)')


async def db_meta_person_by_guid(self, db_connection, guid):
    """
    # return person data
    """
    return await db_connection.fetchrow('select mmp_id, mmp_person_media_id,'
                                        ' mmp_person_meta_json,'
                                        ' mmp_person_image, mmp_person_name,'
                                        ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                        ' from mm_metadata_person where mmp_id = $1', guid)


async def db_meta_person_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of people
    """
    # TODO order by birth date
    if search_value is not None:
        return await db_connection.fetch('select mmp_id,mmp_person_name,'
                                         ' mmp_person_image,'
                                         ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                         ' from mm_metadata_person where mmp_person_name % $1'
                                         ' order by LOWER(mmp_person_name) offset $2 limit $3',
                                         search_value, offset, records)
    else:
        return await db_connection.fetch('select mmp_id,mmp_person_name,mmp_person_image,'
                                         ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                         ' from mm_metadata_person order by LOWER(mmp_person_name)'
                                         ' offset $1 limit $2', offset, records)


async def db_meta_person_list_count(self, db_connection, search_value=None):
    """
    # count person metadata
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_metadata_person'
                                            ' where mmp_person_name % $1', search_value)
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_person')
