import inspect

from common import common_logging_elasticsearch_httpx


async def db_meta_sports_guid_by_thesportsdb(self, thesports_uuid, db_connection=None):
    """
    # metadata guid by thesportsdb id
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
        return await db_conn.fetchval('select count(*) from mm_metadata_sports'
                                      ' where mm_metadata_sports_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*) from mm_metadata_sports')


def db_meta_sports_guid_by_event_name(self, event_name):
    """
    # fetch guid by event name
    """
    self.db_cursor.execute('select mm_metadata_sports_guid'
                           ' from mm_metadata_sports'
                           ' where mm_metadata_sports_name = %s', (event_name,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_sports_guid']
    except:
        return None



def db_metathesportsdb_select_guid(self, guid):
    """
    # select
    """
    self.db_cursor.execute('select mm_metadata_sports_json'
                           ' from mm_metadata_sports'
                           ' where mm_metadata_sports_guid = %s', (guid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_sports_json']
    except:
        return None


def db_metathesportsdb_insert(self, series_id_json, event_name, show_detail,
                              image_json):
    """
    # insert
    """
    new_guid = uuid.uuid4()
    self.db_cursor.execute('insert into mm_metadata_sports (mm_metadata_sports_guid,'
                           ' mm_metadata_media_sports_id,'
                           ' mm_metadata_sports_name,'
                           ' mm_metadata_sports_json,'
                           ' mm_metadata_sports_image_json)'
                           ' values (%s,%s,%s,%s,%s)',
                           (new_guid, series_id_json, event_name, show_detail, image_json))
    self.db_commit()
    return new_guid


def db_metathesports_update(self, series_id_json, event_name, show_detail,
                            sportsdb_id):
    """
    # updated
    """
    self.db_cursor.execute('update mm_metadata_sports'
                           ' set mm_metadata_media_sports_id = %s,'
                           ' mm_metadata_sports_name = %s,'
                           ' mm_metadata_sports_json = %s'
                           ' where mm_metadata_media_sports_id->\'thesportsdb\' ? %s',
                           (series_id_json, event_name, show_detail, sportsdb_id))
    self.db_commit()
