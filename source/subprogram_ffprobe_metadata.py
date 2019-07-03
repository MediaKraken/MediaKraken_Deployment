import functools
import json
import os
import subprocess
import time
import uuid

import pika
from common import common_config_ini
from common import common_ffmpeg
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata
from common import common_network
from common import common_signal

# https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_ffprobe')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


class MKConsumer:
    EXCHANGE = 'mkque_ffmpeg_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkffmpeg'
    ROUTING_KEY = 'mkffmpeg'

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
                'ffprobe': 'Connection is closing or already closed'})
        else:
            common_global.es_inst.com_elastic_index('info', {'ffprobe': 'Closing connection'})
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        common_global.es_inst.com_elastic_index('info', {'ffprobe': 'Closing opened'})
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        common_global.es_inst.com_elastic_index('info',
                                                {'ffprobe': ('Connection open failed: %s', err)})
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            common_global.es_inst.com_elastic_index('info',
                                                    {'ffprobe': (
                                                        'Connection closed, reconnect necessary: %s',
                                                        reason)})
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        common_global.es_inst.com_elastic_index('info', {'ffprobe': 'Creating a new channel'})
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        common_global.es_inst.com_elastic_index('info', {'ffprobe': 'Channel opened'})
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        common_global.es_inst.com_elastic_index('info',
                                                {'ffprobe': 'Adding channel close callback'})
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': ('Channel %i was closed: %s', channel, reason)})
        self.close_connection()

    def setup_exchange(self, exchange_name):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': ('Declaring exchange: %s', exchange_name)})
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
                                                {'ffprobe': ('Exchange declared: %s', userdata)})
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        common_global.es_inst.com_elastic_index('info',
                                                {'ffprobe': ('Declaring queue %s', queue_name)})
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        common_global.es_inst.com_elastic_index('info', {'ffprobe': ('Binding %s to %s with %s',
                                                                     self.EXCHANGE, queue_name,
                                                                     self.ROUTING_KEY)})
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        common_global.es_inst.com_elastic_index('info', {'ffprobe': ('Queue bound: %s', userdata)})
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': ('QOS set to: %d', self._prefetch_count)})
        self.start_consuming()

    def start_consuming(self):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': 'Issuing consumer related RPC commands'})
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': 'Adding consumer cancellation callback'})
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': ('Consumer was cancelled remotely, shutting down: %r', method_frame)})
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        # LOGGER.info('Received message # %s from %s: %s',
        #             basic_deliver.delivery_tag, properties.app_id, body)
        if body is not None:
            json_message = json.loads(body)
            common_global.es_inst.com_elastic_index('info', {'ffprobe': json_message})
            ffprobe_data = common_ffmpeg.com_ffmpeg_media_attr(json_message['Media Path'])
            common_global.es_inst.com_elastic_index('info', {'ffprobe_data': ffprobe_data})
            # check for none first as it might be invalid json
            if ffprobe_data is not None:
                ffprobe_data = json.loads(ffprobe_data)
                # begin image generation
                chapter_image_list = {}
                chapter_count = 0
                first_image = True
                # do this check as not all media has chapters....like LD rips
                if 'chapters' in ffprobe_data:
                    for chapter_data in ffprobe_data['chapters']:
                        chapter_count += 1
                        # file path, time, output name
                        # check image save option whether to save this in media folder or metadata folder
                        if option_config_json['Metadata']['MetadataImageLocal'] is False:
                            image_file_path = os.path.join(
                                common_metadata.com_meta_image_file_path(json_message['Media Path'],
                                                                         'chapter'),
                                (str(uuid.uuid4()) + '.png'))
                        else:
                            image_file_path = os.path.join(
                                os.path.dirname(json_message['Media Path']),
                                'chapters')
                            # have this bool so I don't hit the os looking for path each time
                            if first_image == True and not os.path.isdir(image_file_path):
                                os.makedirs(image_file_path)
                            image_file_path = os.path.join(
                                image_file_path, (str(chapter_count) + '.png'))
                        command_list = []
                        command_list.append('ffmpeg')
                        # if ss is before the input it seeks and doesn't convert every frame like after input
                        command_list.append('-ss')
                        # format the seconds to what ffmpeg is looking for
                        minutes, seconds = divmod(float(chapter_data['start_time']), 60)
                        hours, minutes = divmod(minutes, 60)
                        command_list.append("%02d:%02d:%02f" % (hours, minutes, seconds))
                        command_list.append('-i')
                        command_list.append('\"' + json_message['Media Path'] + '\"')
                        command_list.append('-vframes')
                        command_list.append('1')
                        command_list.append('\"' + image_file_path + '\"')
                        ffmpeg_proc = subprocess.Popen(command_list, stdout=subprocess.PIPE,
                                                       shell=False)
                        ffmpeg_proc.wait()  # wait for subprocess to finish to not flood with ffmpeg processes

                        # as the worker might see it as finished if allowed to continue
                        chapter_image_list[chapter_data['tags']['title']] = image_file_path
                        first_image = False
                # TODO this should be merged into one database update
                db_connection.db_update_media_json(json_message['Media UUID'],
                                                   json.dumps(
                                                       {'ChapterImages': chapter_image_list}))
                db_connection.db_media_ffmeg_update(json_message['Media UUID'],
                                                    json.dumps(ffprobe_data))
            else:
                common_global.es_inst.com_elastic_index('error', {'ffprobe': json_message})
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        common_global.es_inst.com_elastic_index('error', {
            'ffprobe': ('Acknowledging message %s', delivery_tag)})
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            common_global.es_inst.com_elastic_index('error',
                                                    {
                                                        'ffprobe': 'Sending a Basic.Cancel RPC command to RabbitMQ'})
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        common_global.es_inst.com_elastic_index('info', {
            'ffprobe': ('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)})
        self.close_channel()

    def close_channel(self):
        common_global.es_inst.com_elastic_index('error', {'ffprobe': 'Closing the channel'})
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            common_global.es_inst.com_elastic_index('error', {'ffprobe': 'Stopping'})
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            common_global.es_inst.com_elastic_index('error', {'ffprobe': 'Stopped'})

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
                                                        {'ffprobe': (
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
    # fire off wait for it script to allow connection
    common_network.mk_network_service_available('mkrabbitmq', '5672')
    mk_rabbit = MKConsumer('amqp://guest:guest@mkrabbitmq:5672/%2F')
    try:
        mk_rabbit.run()
    except KeyboardInterrupt:
        mk_rabbit.stop()


if __name__ == '__main__':
    main()
