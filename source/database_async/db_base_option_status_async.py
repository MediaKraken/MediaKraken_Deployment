def db_opt_status_read(self, db_connection):
    """
    Read options
    """
    return db_connection.fetch(
        'select mm_options_json, mm_status_json'
        ' from mm_options_and_status')
