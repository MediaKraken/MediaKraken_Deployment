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
import shlex
import subprocess
import time
import uuid

import pika
from common import common_config_ini
from common import common_device_capability
from common import common_docker
from common import common_global
from common import common_logging_elasticsearch
from network import network_base_line as network_base
from pika.adapters import twisted_connection
from twisted.internet import reactor, protocol, defer, task
from twisted.internet import ssl

mk_containers = {}
docker_inst = common_docker.CommonDocker()


@defer.inlineCallbacks
def run(connection):
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 1'})
    channel = yield connection.channel()
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 1.5'})
    exchange = yield channel.exchange_declare(exchange='mkque_ex', exchange_type='direct',
                                              durable=True)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 2'})
    queue = yield channel.queue_declare(queue='mkque', durable=True)
    yield channel.queue_bind(exchange='mkque_ex', queue='mkque')
    yield channel.basic_qos(prefetch_count=1)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 3'})
    queue_object, consumer_tag = yield channel.basic_consume(queue='mkque', no_ack=False)
    l = task.LoopingCall(read, queue_object)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 4'})
    l.start(0.01)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'begin run 5'})


@defer.inlineCallbacks
def read(queue_object):
    global mk_containers
    common_global.es_inst.com_elastic_index('info', {'stuff': 'here I am in consume - read'})
    ch, method, properties, body = yield queue_object.get()

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

    if body:
        common_global.es_inst.com_elastic_index('info', {"body": body})
        # network_base.NetworkEvents.ampq_message_received(body)
        json_message = json.loads(body)
        common_global.es_inst.com_elastic_index('info', {'json body': json_message})
        if json_message['Type'] == 'Cron Run':
            cron_pid = subprocess.Popen(['python3', json_message['Data']])
        elif json_message['Type'] == 'Library Scan':
            scan_pid = subprocess.Popen(['python3', './subprogram_file_scan.py'])
        elif json_message['Type'] == 'Pause':
            if json_message['Subtype'] == 'Cast':
                pass
        elif json_message['Type'] == 'Play':
            # to address the 30 char name limit for container
            name_container = (json_message['User'] + '_'
                              + str(uuid.uuid4()).replace('-', ''))[-30:]
            common_global.es_inst.com_elastic_index('info', {'cont': name_container})
            # TODO only for now until I get the device for websessions (cookie perhaps?)
            if 'Device' in json_message:
                define_new_container = (name_container, json_message['Device'],
                                        json_message['Target'], json_message['Data'])
            else:
                define_new_container = (name_container, None,
                                        json_message['Target'], json_message['Data'])
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
            if json_message['Subtype'] == 'Cast':
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
                container_command = 'castnow --address ' + json_message['Target'] \
                                    + ' --myip 10.0.0.198 ' + subtitle_command \
                                    + ' --ffmpeg \'-c:v copy -c:a ac3' \
                                    + ' --ffmpeg-movflags frag_keyframe+empty_moov+faststart\'' \
                                    + ' --tomp4 \'' + json_message['Data'] + '\''
            elif json_message['Subtype'] == 'Web':
                # stream to web
                container_command = shlex.split("ffmpeg -v fatal {ss_string}"
                                                " -i ".format(**locals())) \
                                    + json_message['Data'] \
                                    + shlex.split("-c:a aac -strict experimental -ac 2 -b:a 64k"
                                                  " -c:v libx264 -pix_fmt yuv420p"
                                                  " -profile:v high -level 4.0"
                                                  " -preset ultrafast -trellis 0"
                                                  " -crf 31 -vf scale=w=trunc(oh*a/2)*2:h=480"
                                                  " -shortest -f mpegts"
                                                  " -output_ts_offset {output_ts_offset:.6f}"
                                                  " -t {t:.6f} pipe:%d.ts".format(**locals()))
            elif json_message['Subtype'] == 'HDHomerun':
                # stream from homerun
                container_command = "ffmpeg -i http://" + json_message['IP'] \
                                    + ":5004/auto/v" + json_message['Channel'] \
                                    + "?transcode=" + json_message['Quality'] + "-vcodec copy" \
                                    + "./static/streams/" + \
                                    json_message['Channel'] + ".m3u8"
                container_command = shlex.split(container_command)
            else:
                common_global.es_inst.com_elastic_index('critical', {'stuff': 'unknown subtype'})
            if container_command is not None:
                common_global.es_inst.com_elastic_index('info',
                                                        {'container_command': container_command,
                                                         'name': name_container})
                hwaccel = False
                docker_inst.com_docker_run_slave(hwaccel=hwaccel,
                                                 name_container=name_container,
                                                 container_command=container_command)
                common_global.es_inst.com_elastic_index('info', {'stuff': 'after docker run'})
        elif json_message['Type'] == 'Stop':
            # this will force stop the container and then delete it
            common_global.es_inst.com_elastic_index('info', {'user stop':
                                                                 mk_containers[
                                                                     json_message['User']]})
            docker_inst.com_docker_delete_container(
                container_image_name=mk_containers[json_message['User']])
        elif json_message['Type'] == 'FFMPEG':
            # to address the 30 char name limit for container
            name_container = ((json_message['User'] + '_'
                               + str(uuid.uuid4()).replace('-', ''))[-30:])
            common_global.es_inst.com_elastic_index('info', {'ffmpegcont': name_container})
            hwaccel = False
            docker_inst.com_docker_run_slave(hwaccel=hwaccel,
                                             name_container=name_container,
                                             container_command=(
                                                     'python3 subprogram_ffprobe_metadata.py %s' %
                                                     json_message['Data']))
            common_global.es_inst.com_elastic_index('info', {'stuff': 'after docker run'})
    yield ch.basic_ack(delivery_tag=method.delivery_tag)


class MediaKrakenServerApp(protocol.ServerFactory):
    def __init__(self):
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {}  # maps user names to network instances
        self.option_config_json, self.db_connection = common_config_ini.com_config_read()
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Ready for twisted connections!'})
        for cast_devices in self.db_connection.db_device_list(device_type='cast'):
            common_global.client_devices.append(('cast', cast_devices))

    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection)


if __name__ == '__main__':
    # fire off wait for it script to allow rabbitmq connection
    wait_pid = subprocess.Popen(['/mediakraken/wait-for-it-ash.sh', '-h',
                                 'mkrabbitmq', '-p', ' 5672'], shell=False)
    wait_pid.wait()

    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
        'subprogram_reactor_line')

    # pika rabbitmq connection
    cc = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection,
                                pika.ConnectionParameters(
                                    credentials=pika.PlainCredentials('guest', 'guest')))
    pika_instance = cc.connectTCP('mkrabbitmq', 5672)
    pika_instance.addCallback(lambda protocol: protocol.ready)
    pika_instance.addCallback(run)

    # setup for the ssl keys
    reactor.listenSSL(8903, MediaKrakenServerApp(),
                      ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
