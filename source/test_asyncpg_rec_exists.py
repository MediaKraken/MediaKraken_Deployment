import asyncio

import asyncpg


###########
# select exists works !!
##########

async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='metaman',
                                 database='postgres',
                                 host='localhost')

    row = await conn.fetchrow('select exists(select 1 from users2 where name = $1 limit 1) limit 1', 'B54ob')
    print(row)

    row = await conn.fetchrow('select exists(select 1 from users2 where name = $1 limit 1) limit 1', 'Bob')
    print(row)

    row = await conn.fetchrow('select exists(select 1 from users2 limit 1) limit 1')
    print(row)

    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
