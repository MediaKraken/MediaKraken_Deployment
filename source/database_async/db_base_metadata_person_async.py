from common import common_global


async def db_meta_person_as_seen_in(self, db_connection, person_guid):
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
        return await db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                         'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\''
                                         ' from mm_metadata_movie where mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'credits\'->\'cast\''
                                         ' @> \'[{"id": %s}]\' order by LOWER(mm_media_name)',
                                         sql_params)
    elif 'tvmaze' in row_data['mmp_person_media_id']:
        sql_params = int(row_data['mmp_person_media_id']['tvmaze']),
        common_global.es_inst.com_elastic_index('info', {'sql paramts': sql_params})
        return await db_connection.fetch('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                                         'mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->\'Poster\''
                                         ' from mm_metadata_tvshow WHERE mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
                                         '->\'_embedded\'->\'cast\' @> \'[{"person": {"id": %s}}]\' order by LOWER(mm_metadata_tvshow_name)',
                                         sql_params)
        # TODO won't this need to be like below?
    elif 'thetvdb' in row_data['mmp_person_media_id']:
        # sql_params = str(row_data[1]['thetvdb']),
        # TODO little bobby tables
        return await db_connection.fetch('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                                         'mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->\'Poster\''
                                         ' from mm_metadata_tvshow where mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
                                         '->\'Cast\'->\'Actor\' @> \'[{"id": \"'
                                         + str(row_data['mmp_person_media_id']['thetvdb'])
                                         + '\"}]\' order by LOWER(mm_metadata_tvshow_name)')  # , sql_params)  #TODO


async def db_meta_person_by_guid(self, db_connection, guid):
    """
    # return person data
    """
    return await db_connection.fetch('select mmp_id, mmp_person_media_id,'
                                     ' mmp_person_meta_json,'
                                     ' mmp_person_image, mmp_person_name,'
                                     ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                     ' from mm_metadata_person where mmp_id = %s', guid)


async def db_meta_person_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of people
    """
    # TODO order by birth date
    if search_value is not None:
        return await db_connection.fetch('select mmp_id,mmp_person_name,'
                                         ' mmp_person_image,'
                                         ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                         ' from mm_metadata_person where mmp_person_name %% %s'
                                         ' order by LOWER(mmp_person_name) offset %s limit %s',
                                         search_value, offset, records)
    else:
        return await db_connection.fetch('select mmp_id,mmp_person_name,mmp_person_image,'
                                         ' mmp_person_meta_json->\'profile_path\' as mmp_meta'
                                         ' from mm_metadata_person order by LOWER(mmp_person_name)'
                                         ' offset %s limit %s', offset, records)


async def db_meta_person_list_count(self, db_connection, search_value=None):
    """
    # count person metadata
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_metadata_person'
                                            ' where mmp_person_name %% %s', search_value)
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_person')
