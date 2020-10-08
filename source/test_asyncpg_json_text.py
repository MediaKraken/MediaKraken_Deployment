import asyncio
import datetime
import json

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

    await conn.execute('CREATE TABLE if not exists users200(id serial PRIMARY KEY,'
                       ' name text, dob date, test_json jsonb)')

    await conn.execute('INSERT INTO users200(name, dob, test_json) VALUES($1, $2, $3)',
                       '1991', datetime.date(1984, 3, 1),
                       json.dumps({'test': {'waffle': 'works'}}))

    # works
    row = await conn.fetchrow('SELECT id, dob, test_json::json'
                              ' FROM users200'
                              ' WHERE test_json->\'test\'->\'waffle\' ? $1', 'works')
    print(row['id'], row['dob'], row['test_json'])

    # runs and returns after turning bob into 1991
    row12 = await conn.fetchrow('SELECT id, name, dob, test_json::json'
                                ' FROM users200'
                                ' WHERE substring(name from 0 for 5) in (\'1991\', \'1992\')')
    print(row12['id'], row12['test_json'])

    # runs and works
    row2 = await conn.fetchrow('SELECT id, dob, test_json::json'
                               ' FROM users200'
                               ' WHERE substring(test_json->\'test\'->>\'waffle\' from 0 for 5)'
                               ' in (\'work\', \'1992\')')
    print(row2['id'], row2['test_json'])

    # print(row['test_json']['test'])

    await conn.execute('drop table users200')
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
