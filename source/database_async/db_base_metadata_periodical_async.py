def db_meta_periodical_by_uuid(self, db_connection, book_uuid):
    """
    grab periodical by uuid
    """
    return db_connection.fetchrow('select mm_metadata_book_json'
                                  ' from mm_metadata_book '
                                  'where mm_metadata_book_guid = %s', (book_uuid,))


def db_meta_periodical_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    periodical list
    """
    # TODO sort by release date
    if search_value is not None:
        return db_connection.fetch('select mm_metadata_book_guid,mm_metadata_book_name '
                                   'from mm_metadata_book where mm_metadata_book_name %% %s'
                                   ' order by mm_metadata_book_name '
                                   'offset %s limit %s', (search_value, offset, records))
    else:
        return db_connection.fetch('select mm_metadata_book_guid,mm_metadata_book_name '
                                   'from mm_metadata_book order by mm_metadata_book_name '
                                   'offset %s limit %s', (offset, records))


def db_meta_periodical_list_count(self, db_connection, search_value=None):
    """
    periodical list count
    """
    if search_value is not None:
        return db_connection.fetchval('select count(*) '
                                      'from mm_metadata_book'
                                      ' where mm_metadata_book_name %% %s',
                                      (search_value,))
    else:
        return db_connection.fetchval('select count(*) from mm_metadata_book')
