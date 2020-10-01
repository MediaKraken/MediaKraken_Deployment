import json
import uuid

import psycopg2.extras

# setup for unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
psycopg2.extras.register_uuid()
psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
# psycopg2.extras.register_default_json(loads=lambda x: x)
sql3_conn = psycopg2.connect(
    "dbname='postgres' user='postgres' host='localhost'"
    " port=5432 password='metaman' connect_timeout=5")

db_cursor = sql3_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

db_cursor.execute('CREATE TABLE if not exists users120(id serial PRIMARY KEY,'
                  ' name text, test_json jsonb, user_id uuid)')
db_cursor.execute('truncate users120')
# uuid and str(uuid) both return as UUID type
# uuid and str(uuid) both return as UUID type
db_cursor.execute('INSERT INTO users120(name, test_json, user_id) VALUES(%s, %s, %s)',
                  ('Bob', json.dumps({'test': 'works'}), uuid.uuid4()))
# uuid and str(uuid) both return as UUID type
# uuid and str(uuid) both return as UUID type
db_cursor.execute('INSERT INTO users120(name, test_json, user_id) VALUES(%s, %s, %s)',
                  ('Bob', json.dumps({'test': 'works'}), str(uuid.uuid4())))
# ERROR uuid is not json serializable
# db_cursor.execute('INSERT INTO users120(name, test_json, user_id) VALUES(%s, %s, %s)',
#                    'Bob', json.dumps({'test': uuid.uuid4()}), uuid.uuid4())
db_cursor.execute('INSERT INTO users120(name, test_json, user_id) VALUES(%s, %s, %s)',
                  ('Bob', json.dumps({'test': str(uuid.uuid4())}), uuid.uuid4()))

db_cursor.execute('SELECT name, test_json, user_id FROM users120')
for row in db_cursor.fetchall():
    print(row, type(row['test_json']), type(row['user_id']))  # shows as dict and UUID
    print(row['test_json']['test'], type(row['test_json']['test']))  # shows as str of course
    # test UUID convert
    print(uuid.UUID('{%s}' % row['user_id']))  # works
# Close the connection.
db_cursor.close()
