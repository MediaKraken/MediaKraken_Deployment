def db_table_count(self, db_connection, table_name):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # TODO little bobby tables
    return db_connection.fetchval('select count(*) from ' + table_name)
