async def db_collection_list(self, offset=None, records=None, search_value=None):
    """
    Return collections list from the database
    """
    if offset is None:
        if search_value is not None:
            return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                                  ' FROM (select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_name % $1'
                                                  ' order by mm_metadata_collection_name)'
                                                  ' as json_data',
                                                  search_value)
        else:
            return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                                  ' FROM (select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json'
                                                  ' from mm_metadata_collection'
                                                  ' order by mm_metadata_collection_name)'
                                                  ' as json_data')
    else:
        if search_value is not None:
            return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                                  ' FROM (select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_guid'
                                                  ' in (select mm_metadata_collection_guid'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_name % $1'
                                                  ' order by mm_metadata_collection_name'
                                                  ' offset $2 limit $3)'
                                                  ' order by mm_metadata_collection_name)'
                                                  ' as json_data',
                                                  search_value, offset, records)
        else:
            return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                                  ' FROM (select mm_metadata_collection_guid,'
                                                  ' mm_metadata_collection_name,'
                                                  ' mm_metadata_collection_imagelocal_json'
                                                  ' from mm_metadata_collection'
                                                  ' where mm_metadata_collection_guid'
                                                  ' in (select mm_metadata_collection_guid'
                                                  ' from mm_metadata_collection'
                                                  ' order by mm_metadata_collection_name'
                                                  ' offset $1 limit $2) '
                                                  'order by mm_metadata_collection_name)'
                                                  ' as json_data',
                                                  offset, records)


async def db_collection_list_count(self, search_value=None):
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_collection'
                                                 ' where mm_metadata_collection_name % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_collection')


async def db_collection_read_by_guid(self, media_uuid):
    """
    Collection details
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_collection_json,'
                                             ' mm_metadata_collection_imagelocal_json'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_guid = $1)'
                                             ' as json_data',
                                             media_uuid)
