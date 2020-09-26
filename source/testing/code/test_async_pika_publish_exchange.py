import asyncio

import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name='mkque_metadata_ex',
                                                  type=aio_pika.ExchangeType.DIRECT,
                                                  durable=True
                                                  )
        queue = await channel.declare_queue(name='themoviedb', durable=True)
        await queue.bind(exchange=exchange, routing_key='themoviedb')
        await exchange.publish(aio_pika.Message(bytes('Hello', 'utf-8'),
                                                content_type='text/plain',
                                                headers={'foo': 'bar'}
                                                ),
                               routing_key='themoviedb'
                               )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
