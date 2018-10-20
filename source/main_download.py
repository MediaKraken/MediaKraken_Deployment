import json
import subprocess
from shlex import split

import pika
import xmltodict
from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_network
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_download')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


class MKConsumer(object):
    EXCHANGE = 'mkque_download_ex'
    EXCHANGE_TYPE = 'direct'
    QUEUE = 'mkdownload'
    ROUTING_KEY = 'mkdownload'

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
            common_global.es_inst.com_elastic_index('info', {'msg body': body})
            json_message = json.loads(body)
            if json_message['Type'] == 'Download':
                # file, image, etc
                if json_message['Subtype'] == 'File':
                    common_network.mk_network_fetch_from_url(json_message['URL'],
                                                             json_message['Local Save Path'])
                elif json_message['Subtype'] == 'Youtube':
                    dl_pid = subprocess.Popen(split(
                        'youtube-dl -i --download-archive /mediakraken/yt_dl_archive.txt ' +
                        json_message['URL']))
                    dl_pid.wait()  # wait for finish so doesn't startup a bunch of dl's
                elif json_message['Subtype'] == 'HDTrailers':
                    data = xmltodict.parse(common_network.mk_network_fetch_from_url(
                        "http://feeds.hd-trailers.net/hd-trailers", None))
                    if data is not None:
                        for item in data['item']:
                            common_global.es_inst.com_elastic_index('info', {'item': item})
                            download_link = None
                            if ('(Trailer' in data['item']['title']
                                and option_config_json['Trailer']['Trailer'] is True) \
                                    or ('(Behind' in data['item']['title']
                                        and option_config_json['Trailer']['Behind'] is True) \
                                    or ('(Clip' in data['item']['title']
                                        and option_config_json['Trailer']['Clip'] is True) \
                                    or ('(Featurette' in data['item']['title']
                                        and option_config_json['Trailer']['Featurette'] is True) \
                                    or ('(Carpool' in data['item']['title']
                                        and option_config_json['Trailer']['Carpool'] is True):
                                for trailer_url in data['item']['enclosure url']:
                                    if '1080p' in trailer_url:
                                        download_link = data['item']['enclosure url']
                                        break
                            if download_link is not None:
                                # TODO let the metadata fetch program grab these
                                # TODO verify this trailer has not been downloaded before
                                # TODO so only insert db dl records
                                common_network.mk_network_fetch_from_url(
                                    download_link, '/static/meta/trailer')
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
    # set signal exit breaks
    common_signal.com_signal_set_break()
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
