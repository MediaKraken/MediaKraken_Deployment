import asyncio

import aiohttp
from ytpy import YoutubeClient


async def main(loop):
    session = aiohttp.ClientSession()

    client = YoutubeClient(session)

    response = await client.search('chico love letter')
    print(response)

    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
