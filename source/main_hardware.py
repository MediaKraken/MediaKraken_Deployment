"""
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
"""

import functools
import json
import subprocess

import pika
import time
from common import common_global
from common import common_hardware_hue
from common import common_logging_elasticsearch
from common import common_network
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_hardware')


class MKConsumer:
    EXCHANGE = 'mkque_hardware_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkhardware'
    ROUTING_KEY = 'mkhardware'

    def __init__(self, amqp_url):
        self.should_reconnect = False
        self.was_consuming = False
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

    def connect(self):
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            common_global.es_inst.com_elastic_index('info', {
                'hardware': 'Connection is closing or already closed'})
        else:
            common_global.es_inst.com_elastic_index('info', {'hardware': 'Closing connection'})
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        common_global.es_inst.com_elastic_index('info', {'hardware': 'Closing opened'})
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        common_global.es_inst.com_elastic_index('info',
                                                {'hardware': ('Connection open failed: %s', err)})
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            common_global.es_inst.com_elastic_index('info',
                                                    {'hardware': (
                                                        'Connection closed, reconnect necessary: %s',
                                                        reason)})
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        common_global.es_inst.com_elastic_index('info', {'hardware': 'Creating a new channel'})
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        common_global.es_inst.com_elastic_index('info', {'hardware': 'Channel opened'})
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        common_global.es_inst.com_elastic_index('info',
                                                {'hardware': 'Adding channel close callback'})
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': ('Channel %i was closed: %s', channel, reason)})
        self.close_connection()

    def setup_exchange(self, exchange_name):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': ('Declaring exchange: %s', exchange_name)})
        # Note: using functools.partial is not required, it is demonstrating
        # how arbitrary data can be passed to the callback when it is called
        cb = functools.partial(
            self.on_exchange_declareok, userdata=exchange_name)
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=self.EXCHANGE_TYPE,
            callback=cb,
            durable=True)

    def on_exchange_declareok(self, _unused_frame, userdata):
        common_global.es_inst.com_elastic_index('info',
                                                {'hardware': ('Exchange declared: %s', userdata)})
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        common_global.es_inst.com_elastic_index('info',
                                                {'hardware': ('Declaring queue %s', queue_name)})
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        common_global.es_inst.com_elastic_index('info', {'hardware': ('Binding %s to %s with %s',
                                                                      self.EXCHANGE, queue_name,
                                                                      self.ROUTING_KEY)})
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        common_global.es_inst.com_elastic_index('info', {'hardware': ('Queue bound: %s', userdata)})
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': ('QOS set to: %d', self._prefetch_count)})
        self.start_consuming()

    def start_consuming(self):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': 'Issuing consumer related RPC commands'})
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': 'Adding consumer cancellation callback'})
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        common_global.es_inst.com_elastic_index('info', {
            'hardware': ('Consumer was cancelled remotely, shutting down: %r', method_frame)})
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        if body is not None:
            common_global.es_inst.com_elastic_index('info', {'msg body': body})
            json_message = json.loads(body)
            if json_message['Type'] == 'Hardware':
                if json_message['Subtype'] == 'Lights':
                    if json_message['Hardware'] == 'Hue':
                        hardware_hue = common_hardware_hue.CommonHardwareHue(json_message['Target'])
                        if json_message['Action'] == 'OnOff':
                            hardware_hue.com_hardware_hue_light_set(json_message['LightList'], 'on',
                                                                    json_message['Setting'])
                        elif json_message['Action'] == 'Bright':
                            hardware_hue.com_hardware_hue_light_set(json_message['LightList'],
                                                                    'bri',
                                                                    json_message['Setting'])
            elif json_message['Type'] == 'Hardware Scan':
                hardware_proc = subprocess.Popen('/mediakraken/main_hardware_discover.py',
                                               stdout=subprocess.PIPE,
                                               shell=False)
                #hardware_proc.wait()  # do NOT wait, as it's blocking
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        common_global.es_inst.com_elastic_index('error', {
            'hardware': ('Acknowledging message %s', delivery_tag)})
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            common_global.es_inst.com_elastic_index('error',
                                                    {
                                                        'hardware': 'Sending a Basic.Cancel RPC command to RabbitMQ'})
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        common_global.es_inst.com_elastic_index('info', {
            'hardware': ('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)})
        self.close_channel()

    def close_channel(self):
        common_global.es_inst.com_elastic_index('error', {'hardware': 'Closing the channel'})
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            common_global.es_inst.com_elastic_index('error', {'hardware': 'Stopping'})
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            common_global.es_inst.com_elastic_index('error', {'hardware': 'Stopped'})

    class ReconnectingExampleConsumer:
        """This is an example consumer that will reconnect if the nested
        ExampleConsumer indicates that a reconnect is necessary.
        """

        def __init__(self, amqp_url):
            self._reconnect_delay = 0
            self._amqp_url = amqp_url
            self._consumer = MKConsumer(self._amqp_url)

        def run(self):
            while True:
                try:
                    self._consumer.run()
                except KeyboardInterrupt:
                    self._consumer.stop()
                    break
                self._maybe_reconnect()

        def _maybe_reconnect(self):
            if self._consumer.should_reconnect:
                self._consumer.stop()
                reconnect_delay = self._get_reconnect_delay()
                common_global.es_inst.com_elastic_index('error',
                                                        {'hardware': (
                                                            'Reconnecting after %d seconds',
                                                            reconnect_delay)})
                time.sleep(reconnect_delay)
                self._consumer = MKConsumer(self._amqp_url)

        def _get_reconnect_delay(self):
            if self._consumer.was_consuming:
                self._reconnect_delay = 0
            else:
                self._reconnect_delay += 1
            if self._reconnect_delay > 30:
                self._reconnect_delay = 30
            return self._reconnect_delay


def main():
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # fire off wait for it script to allow connection
    common_network.mk_network_service_available('mkstack_rabbitmq', '5672')
    mk_rabbit = MKConsumer('amqp://guest:guest@mkstack_rabbitmq:5672/%2F')
    try:
        mk_rabbit.run()
    except KeyboardInterrupt:
        mk_rabbit.stop()


if __name__ == '__main__':
    main()
