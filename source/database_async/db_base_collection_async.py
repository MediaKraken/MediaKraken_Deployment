async def db_collection_list(self, db_connection, offset=None, records=None, search_value=None):
    """
    Return collections list from the database
    """
    if offset is None:
        if search_value is not None:
            return await db_connection.fetch('select mm_metadata_collection_guid,'
                                             'mm_metadata_collection_name,'
                                             'mm_metadata_collection_imagelocal_json'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_name % $1'
                                             ' order by mm_metadata_collection_name',
                                             search_value)
        else:
            return await db_connection.fetch('select mm_metadata_collection_guid,'
                                             'mm_metadata_collection_name,'
                                             'mm_metadata_collection_imagelocal_json'
                                             ' from mm_metadata_collection'
                                             ' order by mm_metadata_collection_name')
    else:
        if search_value is not None:
            return await db_connection.fetch('select mm_metadata_collection_guid,'
                                             'mm_metadata_collection_name,'
                                             'mm_metadata_collection_imagelocal_json'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_guid'
                                             ' in (select mm_metadata_collection_guid'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_name % $1'
                                             ' order by mm_metadata_collection_name'
                                             ' offset $2 limit $3) order by mm_metadata_collection_name',
                                             search_value, offset, records)
        else:
            return await db_connection.fetch('select mm_metadata_collection_guid,'
                                             'mm_metadata_collection_name,'
                                             'mm_metadata_collection_imagelocal_json'
                                             ' from mm_metadata_collection'
                                             ' where mm_metadata_collection_guid'
                                             ' in (select mm_metadata_collection_guid'
                                             ' from mm_metadata_collection'
                                             ' order by mm_metadata_collection_name'
                                             ' offset $1 limit $2) order by mm_metadata_collection_name',
                                             offset, records)


async def db_collection_list_count(self, db_connection, search_value=None):
    if search_value is not None:
        return await db_connection.fetchval('select count(*)'
                                            ' from mm_metadata_collection'
                                            ' where mm_metadata_collection_name % $1',
                                            search_value)
    else:
        return await db_connection.fetchval('select count(*)'
                                            ' from mm_metadata_collection')


async def db_collection_read_by_guid(self, db_connection, media_uuid):
    """
    Collection details
    """
    return await db_connection.fetchrow('select mm_metadata_collection_json,'
                                        'mm_metadata_collection_imagelocal_json'
                                        ' from mm_metadata_collection'
                                        ' where mm_metadata_collection_guid = $1', media_uuid)
