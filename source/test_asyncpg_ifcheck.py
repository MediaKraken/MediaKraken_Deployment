import asyncio
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

    # await conn.execute('CREATE TABLE users7(id serial PRIMARY KEY,'
    #                    ' name text, test_json jsonb)')

    await conn.execute('INSERT INTO users7(name, test_json) VALUES($1, $2)',
                       'Bob', json.dumps({'test': 'works'}))

    if await conn.fetchval('SELECT count(*) FROM users7') > 0:
        print('here')

    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
