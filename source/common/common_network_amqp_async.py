import json

import aioamqp


async def com_net_amqp_send(body_data, rabbit_host_name='mkstack_rabbitmq',
                            exchange_name='mkque_ex', route_key='mkque'):
    transport, protocol = await aioamqp.connect(host=rabbit_host_name)
    channel = await protocol.channel()
    await channel.exchange_declare(exchange_name=exchange_name, type_name='direct', durable=True)
    await channel.basic_publish(
        payload=json.dumps(body_data),
        exchange_name=exchange_name,
        routing_key=route_key,
        properties={
            'content_type': 'text/plain',
            'delivery_mode': 2,
        },
    )
    await protocol.close()
    transport.close()
