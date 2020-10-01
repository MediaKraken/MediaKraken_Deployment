import asyncio
import json

import asyncpg


###
# fully working for JSON of row along with valid json load
###

async def main():
    conn = await asyncpg.connect(user='postgres',
                                 password='metaman',
                                 database='postgres',
                                 host='localhost')

    row = await conn.fetchrow('SELECT row_to_json(json_data)'
                              ' FROM(SELECT id, dob, test_json'
                              ' FROM users2 WHERE name = $1) as json_data', 'Bob')

    print(json.loads(row[0])['test_json']['test'])
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
