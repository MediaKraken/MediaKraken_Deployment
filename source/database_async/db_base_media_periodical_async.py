def db_media_book_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    book list
    """
    if search_value is not None:
        return db_connection.fetch('select mm_metadata_book_guid,'
                                   'mm_metadata_book_name '
                                   'from mm_metadata_book, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_book_guid '
                                   ' and mm_metadata_book_name %% %s'
                                   ' order by LOWER(mm_metadata_book_name)'
                                   ' offset %s limit %s', (search_value, offset, records))
    else:
        return db_connection.fetch('select mm_metadata_book_guid,'
                                   'mm_metadata_book_name '
                                   'from mm_metadata_book, mm_media'
                                   ' where mm_media_metadata_guid = mm_metadata_book_guid'
                                   ' order by LOWER(mm_metadata_book_name)'
                                   ' offset %s limit %s', (offset, records))


def db_media_book_list_count(self, db_connection, search_value=None):
    """
    book list count
    """
    if search_value is not None:
        return db_connection.fetchval('select count(*) from mm_metadata_book,'
                                      ' mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_book_guid '
                                      'and mm_metadata_book_name %% %s', (search_value,))
    else:
        return db_connection.fetchval('select count(*) from mm_metadata_book,'
                                      ' mm_media'
                                      ' where mm_media_metadata_guid = mm_metadata_book_guid')
