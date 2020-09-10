async def db_media_book_list(self, offset=0, records=None, search_value=None):
    """
    book list
    """
    if search_value is not None:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_book_guid,'
                                              ' mm_metadata_book_name'
                                              ' from mm_metadata_book, mm_media'
                                              ' where mm_media_metadata_guid'
                                              ' = mm_metadata_book_guid '
                                              ' and mm_metadata_book_name % $1'
                                              ' order by LOWER(mm_metadata_book_name)'
                                              ' offset $2 limit $3) as json_data',
                                              search_value, offset, records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_book_guid,'
                                              ' mm_metadata_book_name'
                                              ' from mm_metadata_book, mm_media'
                                              ' where mm_media_metadata_guid'
                                              ' = mm_metadata_book_guid'
                                              ' order by LOWER(mm_metadata_book_name)'
                                              ' offset $1 limit $2) as json_data',
                                              offset, records)


async def db_media_book_list_count(self, search_value=None):
    """
    book list count
    """
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_book,'
                                                 ' mm_media'
                                                 ' where mm_media_metadata_guid'
                                                 ' = mm_metadata_book_guid '
                                                 'and mm_metadata_book_name % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_book,'
                                                 ' mm_media'
                                                 ' where mm_media_metadata_guid'
                                                 ' = mm_metadata_book_guid')
