# query provided by postgresql wiki
def db_pgsql_row_count(self, db_connection):
    """
    # return tables and row count
    """
    return db_connection.fetch('SELECT nspname AS schemaname,relname,reltuples FROM pg_class C'
                               ' LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)'
                               ' WHERE nspname NOT IN (\'pg_catalog\', \'information_schema\')'
                               ' AND relkind=\'r\' ORDER BY reltuples DESC')


# query provided by postgresql wiki
def db_pgsql_table_sizes(self, db_connection):
    """
    # return tables sizes (includes indexes, etc)
    """
    return db_connection.fetch('SELECT nspname || \'.\' || relname AS "relation",'
                               ' pg_total_relation_size(C.oid) AS "total_size"'
                               ' FROM pg_class C'
                               ' LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)'
                               ' WHERE nspname'
                               ' NOT IN (\'pg_catalog\', \'information_schema\')'
                               ' AND C.relkind <> \'i\''
                               ' AND nspname !~ \'^pg_toast\''
                               ' ORDER BY pg_total_relation_size(C.oid) DESC')
