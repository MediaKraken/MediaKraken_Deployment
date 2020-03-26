async def db_meta_periodical_by_uuid(self, db_connection, book_uuid):
    """
    grab periodical by uuid
    """
    return await db_connection.fetchrow('select mm_metadata_book_json'
                                        ' from mm_metadata_book '
                                        'where mm_metadata_book_guid = %s', (book_uuid,))


async def db_meta_periodical_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    periodical list
    """
    # TODO sort by release date
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_book_guid,mm_metadata_book_name '
                                         'from mm_metadata_book where mm_metadata_book_name %% %s'
                                         ' order by mm_metadata_book_name '
                                         'offset %s limit %s', (search_value, offset, records))
    else:
        return await db_connection.fetch('select mm_metadata_book_guid,mm_metadata_book_name '
                                         'from mm_metadata_book order by mm_metadata_book_name '
                                         'offset %s limit %s', (offset, records))


async def db_meta_periodical_list_count(self, db_connection, search_value=None):
    """
    periodical list count
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) '
                                            'from mm_metadata_book'
                                            ' where mm_metadata_book_name %% %s',
                                            (search_value,))
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_book')
