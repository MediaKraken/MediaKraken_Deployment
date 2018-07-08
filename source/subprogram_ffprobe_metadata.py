import json
import os
import subprocess
import uuid

import pika

from common import common_config_ini
from common import common_ffmpeg
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_ffprobe')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


class MKConsumer(object):
    EXCHANGE = 'mkque_ffmpeg_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkffmpeg'
    ROUTING_KEY = 'mkffmpeg'

    def __init__(self, amqp_url):
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url

    def connect(self):
        return pika.SelectConnection(pika.URLParameters(self._url),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        self.add_on_connection_close_callback()
        self.open_channel()

    def add_on_connection_close_callback(self):
        self._connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self._connection.add_timeout(5, self.reconnect)

    def reconnect(self):
        self._connection.ioloop.stop()
        if not self._closing:
            self._connection = self.connect()
            self._connection.ioloop.start()

    def open_channel(self):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_text):
        self._connection.close()

    def setup_exchange(self, exchange_name):
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       exchange_name,
                                       self.EXCHANGE_TYPE, durable=True)

    def on_exchange_declareok(self, unused_frame):
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        self._channel.queue_declare(self.on_queue_declareok, queue_name, durable=True)

    def on_queue_declareok(self, method_frame):
        self._channel.queue_bind(self.on_bindok, self.QUEUE,
                                 self.EXCHANGE, self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        self.start_consuming()

    def start_consuming(self):
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.on_message,
                                                         self.QUEUE)

    def add_on_cancel_callback(self):
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        if self._channel:
            self._channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        if body is not None:
            json_message = json.loads(body)
            common_global.es_inst.es_index('info', {'ffprobe': json_message})
            ffprobe_data = common_ffmpeg.com_ffmpeg_media_attr(
                db_connection.db_read_media(
                    json_message['Data'])['mm_media_path'])
            # begin image generation
            chapter_image_list = {}
            chapter_count = 0
            first_image = True
            for chapter_data in ffprobe_data['chapters']:
                chapter_count += 1
                # file path, time, output name
                # check image save option whether to save this in media folder or metadata folder
                if option_config_json['MetadataImageLocal'] == False:
                    image_file_path = os.path.join(
                        common_metadata.com_meta_image_file_path(json_message['Media Path'],
                                                                 'chapter'),
                        (str(uuid.uuid4()) + '.png'))
                else:
                    image_file_path = os.path.join(os.path.dirname(json_message['Media Path']),
                                                   'chapters')
                    # have this bool so I don't hit the os looking for path each time
                    if first_image == True and not os.path.isdir(image_file_path):
                        os.makedirs(image_file_path)
                    image_file_path = os.path.join(
                        image_file_path, (str(chapter_count) + '.png'))
                command_list = []
                command_list.append('./bin/ffmpeg')
                # if ss is before the input it seeks and doesn't convert every frame like after input
                command_list.append('-ss')
                # format the seconds to what ffmpeg is looking for
                minutes, seconds = divmod(float(chapter_data['start_time']), 60)
                hours, minutes = divmod(minutes, 60)
                command_list.append("%02d:%02d:%02f" % (hours, minutes, seconds))
                command_list.append('-i')
                command_list.append(json_message['Media Path'])
                command_list.append('-vframes')
                command_list.append('1')
                command_list.append(image_file_path)
                ffmpeg_proc = subprocess.Popen(command_list, shell=False)
                ffmpeg_proc.wait()  # wait for subprocess to finish to not flood with ffmpeg processes
                # as the worker might see it as finished if allowed to continue
                chapter_image_list[chapter_data['tags']['title']] = image_file_path
                first_image = False
            db_connection.db_update_media_json(json_message['Media UUID'],
                                               json.dumps({'ChapterImages': chapter_image_list}))
            db_connection.db_media_ffmeg_update(json_message['Media UUID'],
                                                json.dumps(ffprobe_data))
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        if self._channel:
            self._channel.basic_cancel(self.on_cancelok, self._consumer_tag)

    def on_cancelok(self, unused_frame):
        self.close_channel()

    def close_channel(self):
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        self._closing = True
        self.stop_consuming()
        self._connection.ioloop.start()

    def close_connection(self):
        self._connection.close()


def main():
    # fire off wait for it script to allow rabbitmq connection
    wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                                 'mkrabbitmq', '-p', ' 5672'], shell=False)
    wait_pid.wait()
    mk_rabbit = MKConsumer('amqp://guest:guest@mkrabbitmq:5672/%2F')
    try:
        mk_rabbit.run()
    except KeyboardInterrupt:
        mk_rabbit.stop()


if __name__ == '__main__':
    main()
