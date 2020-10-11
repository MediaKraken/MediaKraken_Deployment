import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_hardware_device_count(self, hardware_manufacturer, model_name=None,
                                   db_connection=None):
    """
    Return json for machine/model
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
    if model_name is None:
        return await db_conn.fetchval('select count(*) from mm_hardware'
                                      ' where mm_hardware_manufacturer = $1',
                                      hardware_manufacturer)
    else:
        return await db_conn.fetchval('select count(*) from mm_hardware'
                                      ' where mm_hardware_manufacturer = $1'
                                      ' and mm_hardware_model = $2',
                                      hardware_manufacturer, model_name)


async def db_hardware_json_read(self, manufacturer, model_name, db_connection=None):
    """
    Return json for machine/model
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
    return await db_conn.fetchval('select mm_hardware_json'
                                  ' from mm_hardware_json'
                                  ' where mm_hardware_manufacturer = $1'
                                  ' and mm_hardware_model = $2',
                                  manufacturer, model_name)


async def db_hardware_insert(self, manufacturer, model_name, json_data, db_connection=None):
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
    new_guid = uuid.uuid4()
    await db_conn.execute('insert into mm_hardware_json (mm_hardware_id,'
                          ' mm_hardware_manufacturer,'
                          ' mm_hardware_model,'
                          ' mm_hardware_json)'
                          ' values ($1, $2, $3, $4)',
                          new_guid, manufacturer, model_name, json_data)
    await db_conn.execute('commit')
    return new_guid


async def db_hardware_delete(self, guid, db_connection=None):
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
    await db_conn.execute('delete from mm_hardware_json'
                          ' where mm_hardware_id = $1', guid)
    await db_conn.execute('commit')
