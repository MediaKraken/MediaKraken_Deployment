import asyncio
import json

import aio_pika

# sends messages to exchange just fine

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

        # await channel.basic_publish(exchange='mkque_metadata_ex',
        #                             routing_key='themoviedb',
        #                             body=json.dumps(
        #                                 {'Type': 'Roku', 'Subtype': 'Thumbnail'}),
        #                             properties=pika.BasicProperties(
        #                                 content_type='text/plain',
        #                                 delivery_mode=2))

        # Sending the message
        await exchange.publish(aio_pika.Message(
            bytes(json.dumps({'Type': 'Roku', 'Subtype': 'Thumbnail'}), 'utf-8'),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key="themoviedb")

        # this sends message
        # await exchange.publish(aio_pika.Message(bytes('Hello', 'utf-8'),
        #                                         content_type='text/plain',
        #                                         headers={'foo': 'bar'}
        #                                         ),
        #                        routing_key='themoviedb'
        #                        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
