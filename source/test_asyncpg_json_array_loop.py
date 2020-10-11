import asyncio
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

    genre_json = {"genres": [{"id": 18, "name": "Drama"}, {"id": 10752, "name": "War"}]}
    print(genre_json)
    genres_list = []
    for ndx in range(0, len(genre_json['genres'])):
        genres_list.append(genre_json['genres'][ndx]['name'])
    print(genres_list)
    # Close the connection.
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
