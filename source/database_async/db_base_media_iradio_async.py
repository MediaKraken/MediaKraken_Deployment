import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_iradio_insert(self, radio_channel, db_connection=None):
    """
    Insert iradio channel
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if await db_conn.fetchval('select count(*) from mm_radio'
                              ' where mm_radio_address = $1',
                              radio_channel) == 0:
        new_guid = str(uuid.uuid4())
        self.db_cursor.execute('insert into mm_radio (mm_radio_guid,'
                               ' mm_radio_address,'
                               ' mm_radio_active)'
                               ' values ($1, $2, true)',
                               new_guid, radio_channel)
        return new_guid


async def db_iradio_list(self, offset=0, records=None, active_station=True,
                         search_value=None, db_connection=None):
    """
    Iradio list
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetch('select mm_radio_guid,'
                                   ' mm_radio_name,'
                                   ' mm_radio_address'
                                   ' from mm_radio where mm_radio_guid'
                                   ' in (select mm_radio_guid from mm_radio'
                                   ' where mm_radio_active = $1 and mm_radio_name % $2'
                                   ' order by LOWER(mm_radio_name) offset $3 limit $4)'
                                   ' order by LOWER(mm_radio_name)',
                                   active_station, search_value, offset, records)
    else:
        return await db_conn.fetch('select mm_radio_guid,'
                                   ' mm_radio_name,'
                                   ' mm_radio_address'
                                   ' from mm_radio where mm_radio_guid'
                                   ' in (select mm_radio_guid'
                                   ' from mm_radio'
                                   ' where mm_radio_active = $1'
                                   ' order by LOWER(mm_radio_name)'
                                   ' offset $2 limit $3)'
                                   ' order by LOWER(mm_radio_name)',
                                   active_station, offset, records)


async def db_iradio_list_count(self, active_station=True, search_value=None, db_connection=None):
    """
    Iradio count
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetchval('select count(*) from mm_radio '
                                      'where mm_radio_active = $1'
                                      ' and mm_radio_name = $2',
                                      active_station)
    else:
        return await db_conn.fetchval('select count(*) from mm_radio'
                                      ' where mm_radio_active = $1',
                                      active_station)
