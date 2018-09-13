'''
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
'''

import json
import os
import signal
import subprocess

import pika
from common import common_global
from common import common_logging_elasticsearch
from common import common_system
from common import common_signal

class MKConsumer(object):
    EXCHANGE = 'mkque_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkque'
    ROUTING_KEY = 'mkque'

    def __init__(self, amqp_url):
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url

    def connect(self):
        common_global.es_inst.com_elastic_index('info', {'Connecting to': self._url})
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Connection opened'})
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        common_global.es_inst.com_elastic_index('info',
                                                {'stuff': 'Adding connection close callback'})
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.
        """
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            common_global.es_inst.com_elastic_index('info',
                                                    {'code': reply_code, 'reply': reply_text})
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self._connection.ioloop.stop()

        if not self._closing:
            # Create a new connection
            self._connection = self.connect()

            # There is now a new connection, needs a new ioloop to run
            self._connection.ioloop.start()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Creating a new channel'})
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Channel opened'})
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Adding channel close callback'})
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param int reply_code: The numeric reason the channel was closed
        :param str reply_text: The text reason the channel was closed

        """
        self._connection.close()

    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.EXCHANGE_TYPE)

    def on_exchange_declareok(self, unused_frame):
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        self._channel.queue_declare(self.on_queue_declareok, queue_name)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        self._channel.queue_bind(self.on_bindok, self.QUEUE,
                                 self.EXCHANGE, self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Queue bound'})
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        common_global.es_inst.com_elastic_index('info',
                                                {'stuff': 'Issuing consumer related RPC commands'})
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.QUEUE)

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        common_global.es_inst.com_elastic_index('info',
                                                {'stuff': 'Adding consumer cancellation callback'})
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        if self._channel:
            self._channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
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
        common_global.es_inst.com_elastic_index('info', {'message': basic_deliver.delivery_tag,
                                                         'from': properties.app_id})
        json_message = json.loads(body)
        if json_message['Type'] != "Image":
            common_global.es_inst.com_elastic_index('info', {'Got Message': body})
        common_global.es_inst.com_elastic_index('info', {'len total': len(body)})

        msg = None
        if json_message['Type'] == "Play":
            if json_message['Device Type'] == 'Cast':
                pass
                # if json_message['Command'] == "Chapter Back":
                #     pass
                # elif json_message['Command'] == "Chapter Forward":
                #     pass
                # elif json_message['Command'] == "Fast Forward":
                #     pass
                # elif json_message['Command'] == "Mute":
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-mute'), shell=False)
                # elif json_message['Command'] == "Pause":
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-pause'), shell=False)
                # elif json_message['Command'] == "Rewind":
                #     pass
                # elif json_message['Command'] == 'Stop':
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-stop'), shell=False)
                # elif json_message['Command'] == "Volume Down":
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-voldown'), shell=False)
                # elif json_message['Command'] == "Volume Set":
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-setvol', json_message['Data']),
                #         shell=False)
                # elif json_message['Command'] == "Volume Up":
                #     subprocess.Popen(
                #         ('python', '/mediakraken/stream2chromecast/stream2chromecast.py',
                #          '-devicename', json_message['Device'], '-volup'), shell=False)
            elif json_message['Device Type'] == 'HDHomeRun':
                pass
            elif json_message['Device Type'] == 'Slave':
                if json_message['Command'] == "Chapter Back":
                    pass
                elif json_message['Command'] == "Chapter Forward":
                    pass
                elif json_message['Command'] == "Fast Forward":
                    pass
                elif json_message['Command'] == "Pause":
                    pass
                elif json_message['Command'] == 'Play':
                    self.proc_ffmpeg_stream = subprocess.Popen(
                        (''), shell=False)
                elif json_message['Command'] == "Rewind":
                    pass
                elif json_message['Command'] == 'Stop':
                    os.killpg(self.proc_ffmpeg_stream.pid, signal.SIGTERM)
        elif json_message['Type'] == "System":
            if json_message['Subtype'] == 'CPU':
                msg = json.dumps({'Type': 'System', 'Sub': 'CPU',
                                  'Data': common_system.com_system_cpu_usage(False)})
            elif json_message['Subtype'] == "Disk":
                msg = json.dumps({'Type': 'System', 'Sub': 'Disk',
                                  'Data': common_system.com_system_disk_usage_all(True)})
            elif json_message['Subtype'] == "MEM":
                msg = json.dumps({'Type': 'System', 'Sub': 'MEM',
                                  'Data': common_system.com_system_virtual_memory(False)})
            elif json_message['Subtype'] == "SYS":
                msg = json.dumps({'Type': 'System', 'Action': 'SYS',
                                  'Data': common_system.com_system_cpu_usage(True),
                                  'Data2': common_system.com_system_disk_usage_all(True),
                                  'Data3': common_system.com_system_virtual_memory(False)})
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        common_global.es_inst.com_elastic_index('info', {'Acknowledging message': delivery_tag})
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method unused_frame: The Basic.CancelOk frame

        """
        common_global.es_inst.com_elastic_index('info', {
            'stuff': 'RabbitMQ acknowledged the cancellation of the consumer'})
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Closing the channel'})
        self._channel.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Closing connection'})
        self._connection.close()


def main():
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_slave')

    # set signal exit breaks
    common_signal.com_signal_set_break()

    # fire off wait for it script to allow rabbitmq connection
    wait_pid = subprocess.Popen(
        ['/mediakraken/wait-for-it-ash.sh', '-h', 'mkrabbitmq', '-p', ' 5672'],
        shell=False)
    wait_pid.wait()

    mkconsume = MKConsumer('amqp://guest:guest@mkrabbitmq:5672/%2F')
    try:
        mkconsume.run()
    except KeyboardInterrupt:
        mkconsume.stop()


if __name__ == '__main__':
    main()
