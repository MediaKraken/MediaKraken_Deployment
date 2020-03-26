async def db_meta_sports_guid_by_thesportsdb(self, db_connection, thesports_uuid):
    """
    # metadata guid by thesportsdb id
    """
    return await db_connection.fetchval('select mm_metadata_sports_guid'
                                        ' from mm_metadata_sports'
                                        ' where mm_metadata_media_sports_id->\'thesportsdb\' ? %s',
                                        (thesports_uuid,))


async def db_meta_sports_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of sporting events
    # TODO order by year
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_sports_guid,'
                                         ' mm_metadata_sports_name'
                                         ' from mm_metadata_sports'
                                         ' where mm_metadata_sports_guid'
                                         ' in (select mm_metadata_sports_guid from mm_metadata_sports'
                                         ' where mm_metadata_sports_name %% %s'
                                         ' order by LOWER(mm_metadata_sports_name) offset %s limit %s)'
                                         ' order by LOWER(mm_metadata_sports_name)',
                                         (search_value, offset, records))
    else:
        return await db_connection.fetch('select mm_metadata_sports_guid, mm_metadata_sports_name'
                                         ' from mm_metadata_sports where mm_metadata_sports_guid'
                                         ' in (select mm_metadata_sports_guid from mm_metadata_sports'
                                         ' order by LOWER(mm_metadata_sports_name) offset %s limit %s)'
                                         ' order by LOWER(mm_metadata_sports_name)',
                                         (offset, records))


async def db_meta_sports_list_count(self, db_connection, search_value=None):
    """
    Count sport events
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_metadata_sports'
                                            ' where mm_metadata_sports_name %% %s', (search_value,))
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_sports')
