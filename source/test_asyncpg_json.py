import asyncio
import datetime
import json

import asyncpg


###
# fully working for DICT of row along with auto json decode/encode
###

async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='metaman',
                                 database='postgres',
                                 host='localhost')

    await conn.set_type_codec('json',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog')

    await conn.execute('CREATE TABLE users2(id serial PRIMARY KEY,'
                       ' name text, dob date, test_json jsonb)')

    await conn.execute('INSERT INTO users2(name, dob, test_json) VALUES($1, $2, $3)',
                       'Bob', datetime.date(1984, 3, 1), json.dumps({'test': 'works'}))

    # shows that one CANNOT use ::json in the insert
    # await conn.execute('INSERT INTO users2(name, test_json::json) VALUES($1, $2)',
    #                    'Bob', {'test': 'works'})

    # shows that one CANNOT use ::json in the update
    # await conn.execute('update users2 set name = $1, test_json::json = $2',
    #                    'Bob', json.dumps({'test': 'works'}))

    row = await conn.fetchrow('SELECT id, dob, test_json::json'
                              ' FROM users2 WHERE name = $1', 'Bob')

    print(row['id'], row['dob'], row['test_json'])
    print(row['test_json']['test'])
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
