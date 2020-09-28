import asyncio
import json
from common import common_logging_elasticsearch_httpx
import aio_pika
from common import common_network


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process(ignore_processed=True):
        try:
            json_message = json.loads(message.body)
            print(json_message)
        except json.decoder.JSONDecodeError as e:
            print('json error:', message.body)
            await message.reject()
            return
        await message.ack()
        await asyncio.sleep(1)


async def main(loop):
    # start up rabbitmq
    connection = await aio_pika.connect_robust("amqp://guest:guest@mkstack_rabbitmq:5672/%2F",
                                               loop=loop)
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    # Declaring exchange
    exchange = await channel.declare_exchange(name='mkque_transcode_ex',
                                              type=aio_pika.ExchangeType.DIRECT,
                                              durable=True)
    # Declaring queue
    queue = await channel.declare_queue(name='transcode',
                                        durable=True)
    # Binding queue
    await queue.bind(exchange=exchange,
                     routing_key='mkque_transcode_ex')
    # Start listening
    await queue.consume(on_message)


if __name__ == "__main__":
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='START',
                                                         index_name='transcode')
    # fire off wait for it script to allow connection
    common_network.mk_network_service_available('mkstack_rabbitmq', '5672')
    # start up the async loop and launch
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
