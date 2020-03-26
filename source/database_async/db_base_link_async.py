async def db_link_delete(self, db_connection, sync_guid):
    """
    Delete server link
    """
    await db_connection.execute('delete from mm_link where mm_link_guid = $1', (sync_guid,))


async def db_link_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    Return list of linked server
    Complete list for admins
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_link_guid,'
                                         ' mm_link_name,'
                                         ' mm_link_json'
                                         ' from mm_link'
                                         ' where mm_link_guid in (select mm_link_guid'
                                         ' from mm_link'
                                         ' where mm_link_name %% $1 offset $2 limit $3)',
                                         (search_value, offset, records))
    else:
        return await db_connection.fetch('select mm_link_guid,'
                                         ' mm_link_name,'
                                         ' mm_link_json'
                                         ' from mm_link'
                                         ' where mm_link_guid in (select mm_link_guid from mm_link'
                                         ' offset $1 limit $2)', (offset, records))


async def db_link_list_count(self, db_connection, search_value=None):
    """
    Return count of linked servers
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*)'
                                            ' from mm_link where mm_link_name %% $1',
                                            (search_value,))
    else:
        return await db_connection.fetchval('select count(*) from mm_link')
