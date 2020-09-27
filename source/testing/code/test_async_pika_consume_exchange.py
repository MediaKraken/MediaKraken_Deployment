import asyncio
import json

import aio_pika


# grabs the messages but errors with already processed with the ACK in there

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            json_message = json.loads(message.body)
            print(json_message)
        except json.decoder.JSONDecodeError as e:
            print('json error:', message.body)
            return
        #await message.ack()
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


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())