import asyncio
import json
import uuid

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

    # await conn.execute('CREATE TABLE users9(id serial PRIMARY KEY,'
    #                    ' name text, user_id uuid)')
    #
    # await conn.execute('INSERT INTO users9(name, user_id) VALUES($1, $2)',
    #                    'Bob', str(uuid.uuid4()))

    delete_me = (await conn.fetchrow('SELECT user_id FROM users9'))
    print(delete_me['user_id'])

    await conn.execute('delete from users9 where user_id = $1', delete_me['user_id'])
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
