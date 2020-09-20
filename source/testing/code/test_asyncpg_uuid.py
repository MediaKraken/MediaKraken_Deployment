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

    x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
    print(x, type(x))

    for row in await conn.fetch('SELECT name, test_json::json, user_id FROM users20'):
        print(row, type(row['test_json']), row['user_id'])  # shows as dict
        print(row['test_json']['test'], type(row['test_json']['test']))  # shows as str of course
        # test UUID convert
        # print(uuid.UUID(row['user_id']))  # no works
        # print(uuid.UUID(row['user_id'].replace('-', '')))  # no work
        # print(uuid.UUID('\'{' + row['test_json']['user_id'] + '}\''))  # no work
        # print(uuid.UUID('{' + row['user_id'] + '}'))  # no work
        print(uuid.UUID('{%s}' % row['user_id']))  # works
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
