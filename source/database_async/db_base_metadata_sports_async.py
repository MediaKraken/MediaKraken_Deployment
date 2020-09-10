async def db_meta_sports_guid_by_thesportsdb(self, thesports_uuid):
    """
    # metadata guid by thesportsdb id
    """
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_sports_guid'
                                             ' from mm_metadata_sports'
                                             ' where mm_metadata_media_sports_id->\'thesportsdb\''
                                             ' ? $1) as json_data',
                                             thesports_uuid)


async def db_meta_sports_list(self, offset=0, records=None, search_value=None):
    """
    # return list of sporting events
    # TODO order by year
    """
    if search_value is not None:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_sports_guid,'
                                              ' mm_metadata_sports_name'
                                              ' from mm_metadata_sports'
                                              ' where mm_metadata_sports_guid'
                                              ' in (select mm_metadata_sports_guid'
                                              ' from mm_metadata_sports'
                                              ' where mm_metadata_sports_name % $1'
                                              ' order by LOWER(mm_metadata_sports_name)'
                                              ' offset $2 limit $3)'
                                              ' order by LOWER(mm_metadata_sports_name))'
                                              ' as json_data',
                                              search_value, offset, records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_sports_guid,'
                                              ' mm_metadata_sports_name'
                                              ' from mm_metadata_sports'
                                              ' where mm_metadata_sports_guid'
                                              ' in (select mm_metadata_sports_guid'
                                              ' from mm_metadata_sports'
                                              ' order by LOWER(mm_metadata_sports_name)'
                                              ' offset $1 limit $2)'
                                              ' order by LOWER(mm_metadata_sports_name))'
                                              ' as json_data',
                                              offset, records)


async def db_meta_sports_list_count(self, search_value=None):
    """
    Count sport events
    """
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_sports'
                                                 ' where mm_metadata_sports_name % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_sports')
