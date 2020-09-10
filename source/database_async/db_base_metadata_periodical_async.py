async def db_meta_periodical_by_uuid(self, book_uuid):
    """
    grab periodical by uuid
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_book_json'
                                             ' from mm_metadata_book'
                                             ' where mm_metadata_book_guid = $1)'
                                             ' as json_data',
                                             book_uuid)


async def db_meta_periodical_list(self, offset=0, records=None, search_value=None):
    """
    periodical list
    """
    # TODO sort by release date
    if search_value is not None:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_book_guid,'
                                              ' mm_metadata_book_name'
                                              ' from mm_metadata_book'
                                              ' where mm_metadata_book_name % $1'
                                              ' order by mm_metadata_book_name'
                                              ' offset $2 limit $3) as json_data',
                                              search_value,
                                              offset, records)
    else:
        return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                              ' FROM (select mm_metadata_book_guid,'
                                              ' mm_metadata_book_name'
                                              ' from mm_metadata_book'
                                              ' order by mm_metadata_book_name'
                                              ' offset $1 limit $2) as json_data',
                                              offset, records)


async def db_meta_periodical_list_count(self, search_value=None):
    """
    periodical list count
    """
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*)'
                                                 ' from mm_metadata_book'
                                                 ' where mm_metadata_book_name % $1',
                                                 search_value, )
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_book')
