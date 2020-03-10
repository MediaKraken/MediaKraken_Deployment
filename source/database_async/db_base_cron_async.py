import datetime


def db_cron_delete(db_connection, cron_uuid):
    """
    Delete cron job
    """
    db_connection.execute('delete from mm_cron'
                          ' where mm_cron_guid = %s',
                          (cron_uuid,))


def db_cron_info(db_connection, cron_uuid):
    """
    Cron job info
    """
    return db_connection.fetch('select mm_cron_guid,'
                               ' mm_cron_name,'
                               ' mm_cron_description,'
                               ' mm_cron_enabled,'
                               ' mm_cron_schedule,'
                               ' mm_cron_last_run,'
                               ' mm_cron_json'
                               ' from mm_cron'
                               ' where mm_cron_guid = %s', (cron_uuid,))


def db_cron_list(db_connection, enabled_only=False, offset=0, records=None):
    """
    Return cron list
    """
    if not enabled_only:
        return db_connection.fetch('select mm_cron_guid,'
                                   ' mm_cron_name,'
                                   ' mm_cron_description,'
                                   ' mm_cron_enabled,'
                                   ' mm_cron_schedule,'
                                   ' mm_cron_last_run,'
                                   ' mm_cron_json'
                                   ' from mm_cron where mm_cron_guid'
                                   ' in (select mm_cron_guid from mm_cron'
                                   ' order by mm_cron_name offset %s limit %s)'
                                   ' order by mm_cron_name', (offset, records))
    else:
        return db_connection.fetch('select mm_cron_guid,'
                                   ' mm_cron_name,'
                                   ' mm_cron_description,'
                                   ' mm_cron_enabled,'
                                   ' mm_cron_schedule,'
                                   ' mm_cron_last_run,'
                                   ' mm_cron_json'
                                   ' from mm_cron where mm_cron_guid'
                                   ' in (select mm_cron_guid from mm_cron'
                                   ' where mm_cron_enabled = true'
                                   ' order by mm_cron_name offset %s limit %s)'
                                   ' order by mm_cron_name', (offset, records))


def db_cron_list_count(db_connection, enabled_only=False):
    """
    Return number of cron jobs
    """
    if not enabled_only:
        return db_connection.fetchval('select count(*) from mm_cron')
    else:
        return db_connection.fetchval(
            'select count(*) from mm_cron'
            ' where mm_cron_enabled = true')


def db_cron_time_update(db_connection, cron_type):
    """
    Update the datetime in which a cron job was run
    """
    db_connection.execute('update mm_cron set mm_cron_last_run = %s'
                          ' where mm_cron_name = %s',
                          (datetime.datetime.now(), cron_type))
