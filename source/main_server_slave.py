"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
import shlex
import subprocess
import time

import pika
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network
from common import common_signal


class MKConsumer:
    EXCHANGE = 'mkque_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkque'
    ROUTING_KEY = 'mkque'

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
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'slave': 'Connection is closing or already closed'})
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'slave': 'Closing connection'})
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': 'Closing opened'})
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
        {'slave': ('Connection open failed: %s', err)})
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
            {'slave': (
                'Connection closed, reconnect necessary: %s',
                reason)})
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': 'Creating a new channel'})
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': 'Channel opened'})
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
        {'slave': 'Adding channel close callback'})
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('Channel %i was closed: %s', channel, reason)})
        self.close_connection()

    def setup_exchange(self, exchange_name):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('Declaring exchange: %s', exchange_name)})
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
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
        {'slave': ('Exchange declared: %s', userdata)})
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
        {'slave': ('Declaring queue %s', queue_name)})
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('Binding %s to %s with %s',
                      self.EXCHANGE, queue_name,
                      self.ROUTING_KEY)})
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('Queue bound: %s', userdata)})
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('QOS set to: %d', self._prefetch_count)})
        self.start_consuming()

    def start_consuming(self):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': 'Issuing consumer related RPC commands'})
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': 'Adding consumer cancellation callback'})
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('Consumer was cancelled remotely, shutting down: %r', method_frame)})
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'message': basic_deliver.delivery_tag,
            'from': properties.app_id})
        json_message = json.loads(body)
        if json_message['Type'] != "Image":
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={'Got Message': body})
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'len total': len(body)})
        # no need to check types....as if it's here, it's a slave command
        subprocess.Popen(shlex.split(json_message['Command']),
                         stdout=subprocess.PIPE, shell=False)
        # if json_message['Device Type'] == 'Cast':
        #     pass
        # if json_message['Command'] == "Chapter Back":
        #     pass
        # elif json_message['Command'] == "Chapter Forward":
        #     pass
        # elif json_message['Command'] == "Fast Forward":
        #     pass
        # elif json_message['Command'] == "Mute":
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-mute'), stdout=subprocess.PIPE, shell=False)
        # elif json_message['Command'] == "Pause":
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-pause'), stdout=subprocess.PIPE, shell=False)
        # elif json_message['Command'] == "Rewind":
        #     pass
        # elif json_message['Command'] == 'Stop':
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-stop'), stdout=subprocess.PIPE, shell=False)
        # elif json_message['Command'] == "Volume Down":
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-voldown'), stdout=subprocess.PIPE, shell=False)
        # elif json_message['Command'] == "Volume Set":
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-setvol', json_message['Data']),
        #         stdout=subprocess.PIPE, shell=False)
        # elif json_message['Command'] == "Volume Up":
        #     subprocess.Popen(
        #         ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
        #          '-devicename', json_message['Device'], '-volup'), stdout=subprocess.PIPE, shell=False)
        # elif json_message['Device Type'] == 'HDHomeRun':
        #     pass
        # elif json_message['Device Type'] == 'Slave':
        #     if json_message['Command'] == "Chapter Back":
        #         pass
        #     elif json_message['Command'] == "Chapter Forward":
        #         pass
        #     elif json_message['Command'] == "Fast Forward":
        #         pass
        #     elif json_message['Command'] == "Pause":
        #         pass
        #     elif json_message['Command'] == 'Play':
        #         pass
        #     elif json_message['Command'] == "Rewind":
        #         pass
        #     elif json_message['Command'] == 'Stop':
        #         os.killpg(self.proc_ffmpeg_stream.pid, signal.SIGTERM)
        # elif json_message['Type'] == "System":
        #     if json_message['Subtype'] == 'CPU':
        #         msg = json.dumps({'Type': 'System', 'Sub': 'CPU',
        #                           'Data': common_system.com_system_cpu_usage(False)})
        #     elif json_message['Subtype'] == "Disk":
        #         msg = json.dumps({'Type': 'System', 'Sub': 'Disk',
        #                           'Data': common_system.com_system_disk_usage_all(True)})
        #     elif json_message['Subtype'] == "MEM":
        #         msg = json.dumps({'Type': 'System', 'Sub': 'MEM',
        #                           'Data': common_system.com_system_virtual_memory(False)})
        #     elif json_message['Subtype'] == "SYS":
        #         msg = json.dumps({'Type': 'System', 'Action': 'SYS',
        #                           'Data': common_system.com_system_cpu_usage(True),
        #                           'Data2': common_system.com_system_disk_usage_all(True),
        #                           'Data3': common_system.com_system_virtual_memory(False)})
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        common_global.es_inst.com_elastic_index('error', {
            'slave': ('Acknowledging message %s', delivery_tag)})
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            common_global.es_inst.com_elastic_index('error',
                                                    {
                                                        'slave': 'Sending a Basic.Cancel RPC command to RabbitMQ'})
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'slave': ('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)})
        self.close_channel()

    def close_channel(self):
        common_global.es_inst.com_elastic_index('error', {'slave': 'Closing the channel'})
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            common_global.es_inst.com_elastic_index('error', {'slave': 'Stopping'})
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            common_global.es_inst.com_elastic_index('error', {'slave': 'Stopped'})

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
                                                        {'slave': (
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
    # start logging
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text='START')

    # set signal exit breaks
    common_signal.com_signal_set_break()

    # fire off wait for it script to allow connection
    common_network.mk_network_service_available('mkstack_rabbitmq', '5672')

    mkconsume = MKConsumer('amqp://guest:guest@mkstack_rabbitmq:5672/%2F')
    try:
        mkconsume.run()
    except KeyboardInterrupt:
        mkconsume.stop()


if __name__ == '__main__':
    main()
