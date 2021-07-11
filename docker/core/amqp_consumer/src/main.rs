use amiquip::{Connection, ConsumerMessage, ConsumerOptions, QueueDeclareOptions, Result};

fn main() -> Result<()> {
    // Open connection.
    let mut connection = Connection::insecure_open("amqp://guest:guest@mkstack_rabbitmq:5672")?;

    // Open a channel - None says let the library choose the channel ID.
    let channel = connection.open_channel(None)?;

    // Declare the queue.
    let queue = channel.queue_declare("mk_default", QueueDeclareOptions::default())?;

    // Start a consumer.
    let consumer = queue.consume(ConsumerOptions::default())?;

    loop {
        for (i, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    println!("({:>3}) Received [{}]", i, body);

                    /*
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
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={"body": body})
            json_message = json.loads(body)
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={
                                                                     'json body': json_message})
            if json_message['Type'] == 'Cron Run':
                if os.path.splitext(json_message['JSON']['program'])[1] == '.py':
                    subprocess.Popen(['python3', json_message['JSON']['program']],
                                     stdout=subprocess.PIPE, shell=False)
                else:
                    subprocess.Popen(['/usr/sbin', json_message['JSON']['program']],
                                     stdout=subprocess.PIPE, shell=False)
            elif json_message['Type'] == 'Library Scan':
                # This is split out since can be done via admin website and cron jobs
                # TODO launch a container to do this.....so, if it gets stuck the others still go
                subprocess.Popen(['python3', '/mediakraken/subprogram_file_scan.py'],
                                 stdout=subprocess.PIPE, shell=False)
            elif json_message['Type'] == 'Playback':
                if json_message['Subtype'] == 'Play':
                    # to address the 30 char name limit for container
                    name_container = (json_message['User'] + '_'
                                      + str(uuid.uuid4()).replace('-', ''))[:30]
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'cont': name_container})
                    # TODO only for now until I get the device for websessions (cookie perhaps?)
                    if 'Device' in json_message:
                        define_new_container = (name_container, json_message['Device'])
                    else:
                        define_new_container = (name_container, None)
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'def': define_new_container})
                    if json_message['User'] in mk_containers:
                        user_activity_list = mk_containers[json_message['User']]
                        user_activity_list.append(define_new_container)
                        mk_containers[json_message['User']] = user_activity_list
                    else:
                        # "double list" so each one is it's own instance
                        mk_containers[json_message['User']] = (define_new_container)
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'dict': mk_containers})
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
                        common_logging_elasticsearch_httpx.com_es_httpx_post(
                            message_type='critical', message_text=
                            {'stuff': 'unknown subtype'})
                    if container_command is not None:
                        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                             message_text=
                                                                             {
                                                                                 'container_command': container_command,
                                                                                 'name': name_container})
                        hwaccel = False
                        docker_inst.com_docker_run_slave(hwaccel=hwaccel,
                                                         port_mapping=None,
                                                         name_container=name_container,
                                                         container_command=container_command)
                        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                             message_text=
                                                                             {
                                                                                 'stuff': 'after docker run'})
                elif json_message['Subtype'] == 'Stop':
                    # this will force stop the container and then delete it
                    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                         message_text={
                                                                             'user stop':
                                                                                 mk_containers[
                                                                                     json_message[
                                                                                         'User']]})
                    docker_inst.com_docker_delete_container(
                        container_image_name=mk_containers[json_message['User']])
                elif json_message['Subtype'] == 'Pause':
                    if json_message['Device'] == 'Cast':
                        pass

                     */


                    consumer.ack(delivery)?;
                }
                other => {
                    println!("Consumer ended: {:?}", other);
                    break;
                }
            }
        }
    }
    connection.close()
}