
async def on_message(message: aio_pika.IncomingMessage):
    async with message.process(ignore_processed=True):
        try:
            json_message = json.loads(message.body)
            print(json_message)
        except json.decoder.JSONDecodeError as e:
            print('json error:', message.body)
            await message.reject()
            return
        # check which ffmpeg process to run
        if json_message['Type'] == 'Roku':
            if json_message['Subtype'] == 'Thumbnail':
                try:
                    common_hardware_roku_bif.com_roku_create_bif(json_message['Media Path'])
                except struct.error:
                    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                        message_type='error',
                        message_text={
                            'fail bif': json_message})
        elif json_message['Type'] == 'HDHomeRun':
            pass
        elif json_message['Type'] == 'FFMPEG':
            if json_message['Subtype'] == 'Probe':
                # scan media file via ffprobe
                ffprobe_data = common_ffmpeg.com_ffmpeg_media_attr(json_message['Media Path'])
                db_connection.db_media_ffmeg_update(json_message['Media UUID'],
                                                    ffprobe_data)
            elif json_message['Subtype'] == 'Cast':
                if json_message['Command'] == "Chapter Back":
                    pass
                elif json_message['Command'] == "Chapter Forward":
                    pass
                elif json_message['Command'] == "Fast Forward":
                    pass
                elif json_message['Command'] == "Mute":
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-mute'),
                        stdout=subprocess.PIPE, shell=False)
                elif json_message['Command'] == "Pause":
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-pause'),
                        stdout=subprocess.PIPE, shell=False)
                elif json_message['Command'] == "Rewind":
                    pass
                elif json_message['Command'] == 'Stop':
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-stop'),
                        stdout=subprocess.PIPE, shell=False)
                elif json_message['Command'] == "Volume Down":
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-voldown'),
                        stdout=subprocess.PIPE, shell=False)
                elif json_message['Command'] == "Volume Set":
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-setvol', json_message['Data']),
                        stdout=subprocess.PIPE, shell=False)
                elif json_message['Command'] == "Volume Up":
                    subprocess.Popen(
                        ('python3', '/mediakraken/stream2chromecast/stream2chromecast.py',
                         '-devicename', json_message['Device'], '-volup'),
                        stdout=subprocess.PIPE, shell=False)
            elif json_message['Subtype'] == 'ChapterImage':
                ffprobe_data = json_message['Data']
                # begin image generation
                chapter_image_list = {}
                chapter_count = 0
                first_image = True
                # do this check as not all media has chapters....like LD rips
                if 'chapters' in ffprobe_data:
                    for chapter_data in ffprobe_data['chapters']:
                        chapter_count += 1
                        # file path, time, output name
                        # check image save option whether to
                        # save this in media folder or metadata folder
                        if option_config_json['MetadataImageLocal'] is False:
                            image_file_path = os.path.join(
                                common_metadata.com_meta_image_file_path(
                                    json_message['Media Path'],
                                    'chapter'),
                                json_message['Media UUID']
                                + '_' + str(chapter_count)
                                + '.png')
                        else:
                            image_file_path = os.path.join(
                                os.path.dirname(json_message['Media Path']),
                                'chapters')
                            # have this bool so I don't hit the os looking for path each time
                            if first_image is True and not os.path.isdir(image_file_path):
                                os.makedirs(image_file_path)
                            image_file_path = os.path.join(
                                image_file_path, (str(chapter_count) + '.png'))
                        # if ss is before the input it seeks
                        # and doesn't convert every frame like after input
                        command_list = ['ffmpeg', '-ss']
                        # format the seconds to what ffmpeg is looking for
                        minutes, seconds = divmod(float(chapter_data['start_time']), 60)
                        hours, minutes = divmod(minutes, 60)
                        command_list.append("%02d:%02d:%02f" % (hours, minutes, seconds))
                        command_list.append('-i')
                        command_list.append('\"' + json_message['Media Path'] + '\"')
                        command_list.append('-vframes')
                        command_list.append('1')
                        command_list.append('\"' + image_file_path + '\"')
                        ffmpeg_proc = subprocess.Popen(command_list,
                                                       stdout=subprocess.PIPE,
                                                       shell=False)
                        # wait for subprocess to finish to not flood with ffmpeg processes
                        ffmpeg_proc.wait()

                        # as the worker might see it as finished if allowed to continue
                        chapter_image_list[chapter_data['tags']['title']] = image_file_path
                        first_image = False
                db_connection.db_update_media_json(json_message['Media UUID'],
                                                   {'ChapterImages': chapter_image_list})

            elif json_message['Subtype'] == 'Sync':
                ffmpeg_params = ['./bin/ffmpeg', '-i', db_connection.db_media_path_by_uuid(
                    row_data['mm_sync_options_json']['Media GUID'])[0]]
                if row_data['mm_sync_options_json']['Options']['Size'] != "Clone":
                    ffmpeg_params.extend(('-fs',
                                          row_data['mm_sync_options_json']['Options']['Size']))
                if row_data['mm_sync_options_json']['Options']['VCodec'] != "Copy":
                    ffmpeg_params.extend(
                        ('-vcodec', row_data['mm_sync_options_json']['Options']['VCodec']))
                if row_data['mm_sync_options_json']['Options']['AudioChannels'] != "Copy":
                    ffmpeg_params.extend(('-ac',
                                          row_data['mm_sync_options_json']['Options'][
                                              'AudioChannels']))
                if row_data['mm_sync_options_json']['Options']['ACodec'] != "Copy":
                    ffmpeg_params.extend(('-acodec',
                                          row_data['mm_sync_options_json']['Options']['ACodec']))
                if row_data['mm_sync_options_json']['Options']['ASRate'] != 'Default':
                    ffmpeg_params.extend(
                        ('-ar', row_data['mm_sync_options_json']['Options']['ASRate']))
                ffmpeg_params.append(row_data['mm_sync_path_to'] + "."
                                     + row_data['mm_sync_options_json']['Options']['VContainer'])
                common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                     message_text={
                                                                         'ffmpeg': ffmpeg_params})
                ffmpeg_pid = subprocess.Popen(shlex.split(ffmpeg_params),
                                              stdout=subprocess.PIPE, shell=False)
                # output after it gets started
                #  Duration: 01:31:10.10, start: 0.000000, bitrate: 4647 kb/s
                # frame= 1091 fps= 78 q=-1.0 Lsize=    3199kB time=00:00:36.48
                # bitrate= 718.4kbits/s dup=197 drop=0 speed= 2.6x
                media_duration = None
                while True:
                    line = ffmpeg_pid.stdout.readline()
                    if line != '':
                        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                             message_text={
                                                                                 'ffmpeg out': line.rstrip()})
                        if line.find('Duration:') != -1:
                            media_duration = timedelta(
                                float(line.split(': ', 1)[1].split(',', 1)[0]))
                        elif line[0:5] == "frame":
                            time_string = timedelta(float(line.split('=', 5)[5].split(' ', 1)[0]))
                            time_percent = time_string.total_seconds() \
                                           / media_duration.total_seconds()
                            db_connection.db_sync_progress_update(row_data['mm_sync_guid'],
                                                                  time_percent)
                            db_connection.db_commit()
                    else:
                        break
                ffmpeg_pid.wait()
                # deal with converted file
                if row_data['mm_sync_options_json']['Type'] == 'Local File System':
                    # just go along merry way as ffmpeg shoulda output to mm_sync_path_to
                    pass
                elif row_data['mm_sync_options_json']['Type'] == 'Remote Client':
                    XFER_THREAD = common_xfer.FileSenderThread(
                        row_data['mm_sync_options_json']['TargetIP'],
                        row_data['mm_sync_options_json']['TargetPort'],
                        row_data['mm_sync_path_to'] + "."
                        + row_data['mm_sync_options_json']['Options'][
                            'VContainer'],
                        row_data['mm_sync_path_to'])
                else:  # cloud item
                    CLOUD_HANDLE = common_cloud.CommonCloud(option_config_json)
                    CLOUD_HANDLE.com_cloud_file_store(row_data['mm_sync_options_json']['Type'],
                                                      row_data['mm_sync_path_to'],
                                                      row_data['mm_sync_path_to'] + "."
                                                      + row_data['mm_sync_options_json']['Options'][
                                                          'VContainer'].split('/', 1)[1], False)
                db_connection.db_sync_delete(row_data[0])  # guid of sync record
        # completed processing, ack, sleep, exit
        await message.ack()
        await asyncio.sleep(1)
