import inspect
import uuid

from common import common_logging_elasticsearch_httpx


async def db_opt_update(self, option_json, db_connection=None):
    """
    Update option json
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
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json = $1',
                          option_json)


async def db_opt_status_update(self, option_json, status_json, db_connection=None):
    """
    Update option and status json
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
    # no need for where clause as it's only the one record
    await db_conn.execute('update mm_options_and_status'
                          ' set mm_options_json = $1,'
                          ' mm_status_json = $2',
                          option_json, status_json)
    await db_conn.execute('commit')


def db_opt_status_read(self):
    """
    Read options
    """
    self.db_cursor.execute(
        'select mm_options_json, mm_status_json'
        ' from mm_options_and_status')
    return self.db_cursor.fetchone()  # no [0] as two fields


def db_opt_status_update_scan(self, scan_json):
    """
    Update scan info
    """
    # no need for where clause as it's only the one record
    self.db_cursor.execute(
        'update mm_options_and_status'
        ' set mm_status_json = %s', (scan_json,))
    self.db_commit()


def db_opt_status_update_scan_rec(self, dir_path, scan_status, scan_percent):
    """
    Update scan data
    """
    self.db_cursor.execute('select mm_status_json'
                           ' from mm_options_and_status')
    # will always have the one record
    status_json = self.db_cursor.fetchone()['mm_status_json']
    status_json.update(
        {'Scan': {dir_path: {'Status': scan_status, 'Pct': scan_percent}}})

    # how about have the status on the lib record itself
    # then in own thread....no, read to update....just update
    # so faster
    #    json_data = self.db_cursor.fetchone()[0]
    #    json_data.update({'UserStats':{user_id:{'Watched':status_bool}}})
    #    json_data = json.dumps(json_data)

    # no need for where clause as it's only the one record
    self.db_cursor.execute('update mm_options_and_status'
                           ' set mm_status_json = %s',
                           (json.dumps(status_json),))
    # 'update objects set mm_options_and_status=jsonb_set(mm_options_and_status,
    # '{name}', '"Mary"', true)'
    self.db_commit()
