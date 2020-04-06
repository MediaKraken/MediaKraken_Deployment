import uuid


async def db_iradio_insert(self, db_connection, radio_channel):
    """
    Insert iradio channel
    """
    if await db_connection.fetchval('select count(*) from mm_radio'
                                    ' where mm_radio_address = $1',
                                    radio_channel) == 0:
        new_guid = str(uuid.uuid4())
        self.db_cursor.execute('insert into mm_radio (mm_radio_guid,'
                               ' mm_radio_address,'
                               'mm_radio_active)'
                               ' values ($1, $2, true)',
                               new_guid, radio_channel)
        return new_guid


async def db_iradio_list(self, db_connection, offset=0, records=None, active_station=True,
                         search_value=None):
    """
    Iradio list
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_radio_guid,'
                                         ' mm_radio_name,'
                                         ' mm_radio_address'
                                         ' from mm_radio where mm_radio_guid '
                                         'in (select mm_radio_guid from mm_radio'
                                         ' where mm_radio_active = $1 and mm_radio_name = $2'
                                         ' order by LOWER(mm_radio_name) offset $3 limit $4)'
                                         ' order by LOWER(mm_radio_name)',
                                         active_station, search_value, offset, records)
    else:
        return await db_connection.fetch('select mm_radio_guid,'
                                         ' mm_radio_name,'
                                         ' mm_radio_address'
                                         ' from mm_radio where mm_radio_guid'
                                         ' in (select mm_radio_guid'
                                         ' from mm_radio'
                                         ' where mm_radio_active = %s'
                                         ' order by LOWER(mm_radio_name)'
                                         ' offset %s limit %s) order by LOWER(mm_radio_name)',
                                         active_station, offset, records)


async def db_iradio_list_count(self, db_connection, active_station=True, search_value=None):
    """
    Iradio count
    """
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_radio '
                                            'where mm_radio_active = $1 and mm_radio_name = $2',
                                            active_station)
    else:
        return await db_connection.fetchval('select count(*) from mm_radio'
                                            ' where mm_radio_active = $1',
                                            active_station)
