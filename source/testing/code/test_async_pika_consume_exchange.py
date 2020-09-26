import asyncio
import json

import aio_pika


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            json_message = json.loads(message.body)
        except json.decoder.JSONDecodeError as e:
            print('json error')
            return
        print(json_message)
        await aio_pika.IncomingMessage.ack()
        await asyncio.sleep(1)


async def main(loop):
    content_providers = 'themoviedb'

    # start up rabbitmq
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)
    print('here1')
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    print('here2')
    # Declaring exchange
    exchange = await channel.declare_exchange(name='mkque_metadata_ex',
                                              type=aio_pika.ExchangeType.DIRECT,
                                              durable=True)
    print('here3')
    # Declaring queue
    queue = await channel.declare_queue(name=content_providers,
                                        durable=True)
    print('here4')
    # Binding queue
    await queue.bind(exchange=exchange, routing_key='mkque_metadata_ex')
    print('here5')
    # Start listening
    await queue.consume(on_message)
    print('here6')

    # connection = await aio_pika.connect_robust(
    #     "amqp://guest:guest@127.0.0.1/", loop=loop
    # )
    # queue_name = "test_queue"
    # # Creating channel
    # channel = await connection.channel()
    # # Maximum message count which will be
    # # processing at the same time.
    # await channel.set_qos(prefetch_count=1)
    # # Declaring queue
    # queue = await channel.declare_queue(queue_name, auto_delete=True)
    # await queue.consume(on_message)
    # return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
