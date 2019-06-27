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

import functools
import json
import os
import subprocess
import time
import uuid

import pika
from common import common_config_ini
from common import common_device_capability
from common import common_docker
from common import common_global
from common import common_logging_elasticsearch
from common import common_network
from common import common_signal

# https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_pika')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

mk_containers = {}
docker_inst = common_docker.CommonDocker()


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
            common_global.es_inst.com_elastic_index('info', {
                'pika': 'Connection is closing or already closed'})
        else:
            common_global.es_inst.com_elastic_index('info', {'pika': 'Closing connection'})
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        common_global.es_inst.com_elastic_index('info', {'pika': 'Closing opened'})
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': ('Connection open failed: %s', err)})
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            common_global.es_inst.com_elastic_index('info',
                                                    {'pika': (
                                                        'Connection closed, reconnect necessary: %s',
                                                        reason)})
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        common_global.es_inst.com_elastic_index('info', {'pika': 'Creating a new channel'})
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        common_global.es_inst.com_elastic_index('info', {'pika': 'Channel opened'})
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        common_global.es_inst.com_elastic_index('info', {'pika': 'Adding channel close callback'})
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        common_global.es_inst.com_elastic_index('info', {
            'pika': ('Channel %i was closed: %s', channel, reason)})
        self.close_connection()

    def setup_exchange(self, exchange_name):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': ('Declaring exchange: %s', exchange_name)})
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
                                                {'pika': ('Exchange declared: %s', userdata)})
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': ('Declaring queue %s', queue_name)})
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb, durable=True)

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name = userdata
        common_global.es_inst.com_elastic_index('info', {'pika': ('Binding %s to %s with %s',
                                                                  self.EXCHANGE, queue_name,
                                                                  self.ROUTING_KEY)})
        cb = functools.partial(self.on_bindok, userdata=queue_name)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=self.ROUTING_KEY,
            callback=cb)

    def on_bindok(self, _unused_frame, userdata):
        common_global.es_inst.com_elastic_index('info', {'pika': ('Queue bound: %s', userdata)})
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': ('QOS set to: %d', self._prefetch_count)})
        self.start_consuming()

    def start_consuming(self):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': 'Issuing consumer related RPC commands'})
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(
            self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        common_global.es_inst.com_elastic_index('info',
                                                {'pika': 'Adding consumer cancellation callback'})
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        common_global.es_inst.com_elastic_index('info', {
            'pika': ('Consumer was cancelled remotely, shutting down: %r', method_frame)})
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """
        Do I actually launch a docker swarm container that checks for cuda
        and then that launches the slave container with ffmpeg

        # this is for the debian one
        docker run -it --rm $(ls /dev/nvidia* | xargs -I{} echo '--device={}') $(ls /usr/lib/x86_64-linux-gnu/{libcuda,libnvidia}* | xargs -I{} echo '-v {}:{}:ro') mediakraken/mkslavenvidiadebian

        --device /dev/nvidia0:/dev/nvidia0 \
        --device /dev/nvidiactl:/dev/nvidiactl \

        wget http://download.blender.org/peach/bigbuckbunny_movies/big_buck_bunny_1080p_surround.avi
        The minimum required Nvidia driver for nvenc is 378.13 or newer from ffmpeg error
        """
        if body is not None:
            common_global.es_inst.com_elastic_index('info', {"body": body})
            json_message = json.loads(body)
            common_global.es_inst.com_elastic_index('info', {'json body': json_message})
            if json_message['Type'] == 'Cron Run':
                if os.path.splitext(json_message['JSON']['program'])[1] == '.py':
                    subprocess.Popen(['python3', json_message['JSON']['program']], shell=False)
                else:
                    subprocess.Popen(['/usr/sbin', json_message['JSON']['program']], shell=False)
            elif json_message['Type'] == 'Library Scan':
                # This is split out since can be done via admin website and cron jobs
                # TODO launch a container to do this.....so, if it gets stuck the others still go
                subprocess.Popen(['python3', '/mediakraken/subprogram_file_scan.py'], shell=False)
            elif json_message['Type'] == 'Playback':
                if json_message['Subtype'] == 'Play':
                    # to address the 30 char name limit for container
                    name_container = (json_message['User'] + '_'
                                      + str(uuid.uuid4()).replace('-', ''))[:30]
                    common_global.es_inst.com_elastic_index('info', {'cont': name_container})
                    # TODO only for now until I get the device for websessions (cookie perhaps?)
                    if 'Device' in json_message:
                        define_new_container = (name_container, json_message['Device'])
                    else:
                        define_new_container = (name_container, None)
                    common_global.es_inst.com_elastic_index('info', {'def': define_new_container})
                    if json_message['User'] in mk_containers:
                        user_activity_list = mk_containers[json_message['User']]
                        user_activity_list.append(define_new_container)
                        mk_containers[json_message['User']] = user_activity_list
                    else:
                        # "double list" so each one is it's own instance
                        mk_containers[json_message['User']] = (define_new_container)
                    common_global.es_inst.com_elastic_index('info', {'dict': mk_containers})
                    container_command = None
                    if json_message['Device'] == 'Cast':
                        # should only need to check for subs on initial play command
                        if 'Subtitle' in json_message:
                            subtitle_command = ' -subtitles ' + json_message['Subtitle']
                        else:
                            subtitle_command = ''
                        return_video_container, return_video_codec, return_audio_codec, return_audio_channels \
                            = common_device_capability.com_device_compat_best_fit(
                            device_type='Chromecast',
                            device_model=None,
                            video_container=None,
                            video_codec=None,
                            audio_codec=None,
                            audio_channels=None)
                        # TODO take number of channels into account
                        # TODO take the video codec into account
                        container_command = 'castnow --tomp4 --ffmpeg-acodec ac3 --ffmpeg-movflags ' \
                                            'frag_keyframe+empty_moov+faststart --address ' \
                                            + json_message['Target'] + ' --myip ' \
                                            + docker_inst.com_docker_info()['Swarm']['NodeAddr'] \
                                            + subtitle_command + ' \'' + json_message['Data'] + '\''
                        hwaccel = False
                        docker_inst.com_docker_run_cast(hwaccel=hwaccel,
                                                        name_container=name_container,
                                                        container_command=container_command)
                    elif json_message['Device'] == 'HDHomerun':
                        # stream from hdhomerun
                        container_command = "ffmpeg -i http://" + json_message['IP'] \
                                            + ":5004/auto/v" + json_message['Channel'] \
                                            + "?transcode=" + json_message[
                                                'Quality'] + "-vcodec copy" \
                                            + "./static/streams/" + \
                                            json_message['Channel'] + ".m3u8"
                    elif json_message['Device'] == 'HLS':
                        # stream to hls
                        # TODO take the video codec into account
                        container_command = 'ffmpeg -i \"' + json_message['Input File'] \
                                            + '\" -vcodec libx264 -preset veryfast' \
                                            + ' -acodec aac -ac:a:0 2 -vbr 5 ' \
                                            + json_message['Audio Track'] \
                                            + '-vf ' + json_message['Subtitle Track'] \
                                            + ' yadif=0:0:0 ' \
                                            + json_message['Target UUID']
                    elif json_message['Device'] == 'Roku':
                        pass
                    elif json_message['Device'] == 'Web':
                        # stream to web
                        container_command = "ffmpeg -v fatal {ss_string}" \
                                            + " -i ".format(**locals()) \
                                            + json_message['Data'] \
                                            + "-c:a aac -strict experimental -ac 2 -b:a 64k" \
                                              " -c:v libx264 -pix_fmt yuv420p" \
                                              " -profile:v high -level 4.0" \
                                              " -preset ultrafast -trellis 0" \
                                              " -crf 31 -vf scale=w=trunc(oh*a/2)*2:h=480" \
                                              " -shortest -f mpegts" \
                                              " -output_ts_offset {output_ts_offset:.6f}" \
                                              " -t {t:.6f} pipe:%d.ts".format(**locals())
                    else:
                        common_global.es_inst.com_elastic_index('critical',
                                                                {'stuff': 'unknown subtype'})
                    if container_command is not None:
                        common_global.es_inst.com_elastic_index('info',
                                                                {
                                                                    'container_command': container_command,
                                                                    'name': name_container})
                        hwaccel = False
                        docker_inst.com_docker_run_slave(hwaccel=hwaccel,
                                                         port_mapping=None,
                                                         name_container=name_container,
                                                         container_command=container_command)
                        common_global.es_inst.com_elastic_index('info',
                                                                {'stuff': 'after docker run'})
                elif json_message['Subtype'] == 'Stop':
                    # this will force stop the container and then delete it
                    common_global.es_inst.com_elastic_index('info', {
                        'user stop': mk_containers[json_message['User']]})
                    docker_inst.com_docker_delete_container(
                        container_image_name=mk_containers[json_message['User']])
                elif json_message['Subtype'] == 'Pause':
                    if json_message['Device'] == 'Cast':
                        pass
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        common_global.es_inst.com_elastic_index('error', {
            'pika': ('Acknowledging message %s', delivery_tag)})
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            common_global.es_inst.com_elastic_index('error',
                                                    {
                                                        'pika': 'Sending a Basic.Cancel RPC command to RabbitMQ'})
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        common_global.es_inst.com_elastic_index('info', {
            'pika': ('RabbitMQ acknowledged the cancellation of the consumer: %s', userdata)})
        self.close_channel()

    def close_channel(self):
        common_global.es_inst.com_elastic_index('error', {'pika': 'Closing the channel'})
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            common_global.es_inst.com_elastic_index('error', {'pika': 'Stopping'})
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            common_global.es_inst.com_elastic_index('error', {'pika': 'Stopped'})

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
                                                        {'pika': ('Reconnecting after %d seconds',
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
