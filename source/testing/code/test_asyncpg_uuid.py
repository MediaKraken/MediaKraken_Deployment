import asyncio
import json
import uuid

import asyncpg


async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='metaman',
                                 database='postgres',
                                 host='localhost')

    await conn.set_type_codec('json',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog')

    await conn.execute('CREATE TABLE if not exists users20(id serial PRIMARY KEY,'
                       ' name text, test_json jsonb, user_id uuid)')
    await conn.execute('truncate users20')
    # uuid and str(uuid) both return as UUID type
    # uuid and str(uuid) both return as UUID type
    # uuid and str(uuid) both return as UUID type
    # uuid and str(uuid) both return as UUID type
    await conn.execute('INSERT INTO users20(name, test_json, user_id) VALUES($1, $2, $3)',
                       'Bob', json.dumps({'test': 'works'}), str(uuid.uuid4()))

    # ERROR uuid is not json serializable
    # await conn.execute('INSERT INTO users20(name, test_json, user_id) VALUES($1, $2, $3)',
    #                    'Bob', json.dumps({'test': uuid.uuid4()}), str(uuid.uuid4()))

    await conn.execute('INSERT INTO users20(name, test_json, user_id) VALUES($1, $2, $3)',
                       'Bob', json.dumps({'test': str(uuid.uuid4())}), uuid.uuid4())

    for row in await conn.fetch('SELECT name, test_json::json, user_id FROM users20'):
        print(row, type(row['test_json']))  # shows as dict
        print(row['test_json']['test'], type(row['test_json']['test']))  # shows as str of course
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
