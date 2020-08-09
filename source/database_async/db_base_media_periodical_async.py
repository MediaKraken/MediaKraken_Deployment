async def db_media_book_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    book list
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_book_guid,'
                                         'mm_metadata_book_name '
                                         'from mm_metadata_book, mm_media'
                                         ' where mm_media_metadata_guid = mm_metadata_book_guid '
                                         ' and mm_metadata_book_name % $1'
                                         ' order by LOWER(mm_metadata_book_name)'
                                         ' offset $2 limit $3', search_value, offset, records)
    else:
        return await db_connection.fetch('select mm_metadata_book_guid,'
                                         'mm_metadata_book_name '
                                         'from mm_metadata_book, mm_media'
                                         ' where mm_media_metadata_guid = mm_metadata_book_guid'
                                         ' order by LOWER(mm_metadata_book_name)'
                                         ' offset $1 limit $2', offset, records)


async def db_media_book_list_count(self, db_connection, search_value=None):
    """
    book list count
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_metadata_book,'
                                            ' mm_media'
                                            ' where mm_media_metadata_guid = mm_metadata_book_guid '
                                            'and mm_metadata_book_name % $1', search_value)
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_book,'
                                            ' mm_media'
                                            ' where mm_media_metadata_guid = mm_metadata_book_guid')
