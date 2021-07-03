import asyncio
import datetime
import json

import asyncpg


async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='metaman',
                                 database='postgres',
                                 host='localhost')

    await conn.set_type_codec('jsonb',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog')

    await conn.execute('CREATE TABLE users2654(id serial PRIMARY KEY,'
                       ' name text, dob date, test_json jsonb)')

    await conn.execute('INSERT INTO users2654(name, dob, test_json) VALUES($1, $2, $3)',
                       'Bob', datetime.date(1984, 3, 1), json.dumps({'test': 'works'}))

    row = await conn.fetchrow('SELECT id, dob, test_json'
                              ' FROM users2654 WHERE name = $1', 'Bob')

    print(row['id'], row['dob'], row['test_json'])
    # TypeError: string indices must be integers
    print(row['test_json']['test'])

    await conn.execute('drop table users2654')
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
