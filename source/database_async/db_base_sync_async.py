import uuid


def db_sync_delete(self, db_connection, sync_guid):
    """
    # delete sync job
    """
    db_connection.execute(
        'delete from mm_sync'
        ' where mm_sync_guid = %s', (sync_guid,))


def db_sync_insert(self, db_connection, sync_path, sync_path_to, sync_json):
    """
    # insert sync job
    """
    new_guid = str(uuid.uuid4())
    db_connection.execute('insert into mm_sync (mm_sync_guid,'
                          ' mm_sync_path,'
                          ' mm_sync_path_to,'
                          ' mm_sync_options_json)'
                          ' values (%s, %s, %s, %s)', (new_guid, sync_path,
                                                       sync_path_to,
                                                       sync_json))
    return new_guid


def db_sync_list(self, db_connection, offset=0, records=None, user_guid=None):
    """
    # return list of sync jobs
    """
    # TODO by priority, name, year
    if user_guid is None:
        # complete list for admins
        return db_connection.fetch('select mm_sync_guid uuid,'
                                   ' mm_sync_path,'
                                   ' mm_sync_path_to,'
                                   ' mm_sync_options_json'
                                   ' from mm_sync'
                                   ' where mm_sync_guid in (select mm_sync_guid'
                                   ' from mm_sync'
                                   ' order by mm_sync_options_json->\'Priority\''
                                   ' desc, mm_sync_path'
                                   ' offset %s limit %s)'
                                   ' order by mm_sync_options_json->\'Priority\''
                                   ' desc, mm_sync_path', (offset, records))
    else:
        return db_connection.fetch('select mm_sync_guid uuid,'
                                   ' mm_sync_path,'
                                   ' mm_sync_path_to,'
                                   ' mm_sync_options_json'
                                   ' from mm_sync'
                                   ' where mm_sync_guid in (select mm_sync_guid'
                                   ' from mm_sync'
                                   ' where mm_sync_options_json->\'User\'::text = %s'
                                   ' order by mm_sync_options_json->\'Priority\''
                                   ' desc, mm_sync_path  offset %s limit %s)'
                                   ' order by mm_sync_options_json->\'Priority\''
                                   ' desc, mm_sync_path', (str(user_guid), offset, records))
