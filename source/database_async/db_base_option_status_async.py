def db_opt_update(self, db_connection, option_json):
    """
    Update option json
    """
    # no need for where clause as it's only the one record
    db_connection.execute('update mm_options_and_status'
                          ' set mm_options_json = %s',
                          (option_json,))


def db_opt_status_read(self, db_connection):
    """
    Read options
    """
    return db_connection.fetch(
        'select mm_options_json, mm_status_json'
        ' from mm_options_and_status')
