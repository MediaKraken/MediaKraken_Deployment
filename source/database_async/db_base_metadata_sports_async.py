async def db_meta_sports_guid_by_thesportsdb(self, thesports_uuid, db_connection=None):
    """
    # metadata guid by thesportsdb id
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select mm_metadata_sports_guid'
                                  ' from mm_metadata_sports'
                                  ' where mm_metadata_media_sports_id->\'thesportsdb\''
                                  ' ? $1',
                                  thesports_uuid)


async def db_meta_sports_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    # return list of sporting events
    # TODO order by year
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetch('select mm_metadata_sports_guid,'
                                   ' mm_metadata_sports_name'
                                   ' from mm_metadata_sports'
                                   ' where mm_metadata_sports_guid'
                                   ' in (select mm_metadata_sports_guid'
                                   ' from mm_metadata_sports'
                                   ' where mm_metadata_sports_name % $1'
                                   ' order by LOWER(mm_metadata_sports_name)'
                                   ' offset $2 limit $3)'
                                   ' order by LOWER(mm_metadata_sports_name)',
                                   search_value, offset, records)
    else:
        return await db_conn.fetch('select mm_metadata_sports_guid,'
                                   ' mm_metadata_sports_name'
                                   ' from mm_metadata_sports'
                                   ' where mm_metadata_sports_guid'
                                   ' in (select mm_metadata_sports_guid'
                                   ' from mm_metadata_sports'
                                   ' order by LOWER(mm_metadata_sports_name)'
                                   ' offset $1 limit $2)'
                                   ' order by LOWER(mm_metadata_sports_name)',
                                   offset, records)


async def db_meta_sports_list_count(self, search_value=None, db_connection=None):
    """
    Count sport events
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetchval('select count(*) from mm_metadata_sports'
                                      ' where mm_metadata_sports_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*) from mm_metadata_sports')
