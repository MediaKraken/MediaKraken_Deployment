async def db_table_count(db_connection, table_name):
    """
    # return count of records in table
    """
    # can't %s due to ' inserted
    # All table names will be done by server code, little bobby tables shouldn't apply
    return await db_connection.fetchval('select count(*) from ' + table_name)
