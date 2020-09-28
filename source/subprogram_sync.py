# open the database
option_config_json, db_connection = common_config_ini.com_config_read()
# row_data
# 0 mm_sync_guid uuid NOT NULL, 1 mm_sync_path text, 2 mm_sync_path_to text,
# 3 mm_sync_options_json jsonb
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
                          row_data['mm_sync_options_json']['Options']['AudioChannels']))
if row_data['mm_sync_options_json']['Options']['ACodec'] != "Copy":
    ffmpeg_params.extend(('-acodec',
                          row_data['mm_sync_options_json']['Options']['ACodec']))
if row_data['mm_sync_options_json']['Options']['ASRate'] != 'Default':
    ffmpeg_params.extend(
        ('-ar', row_data['mm_sync_options_json']['Options']['ASRate']))
ffmpeg_params.append(row_data['mm_sync_path_to'] + "."
                     + row_data['mm_sync_options_json']['Options']['VContainer'])
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'ffmpeg': ffmpeg_params})
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
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'ffmpeg out': line.rstrip()})
        if line.find("Duration:") != -1:
            media_duration = timedelta(float(line.split(': ', 1)[1].split(',', 1)[0]))
        elif line[0:5] == "frame":
            time_string = timedelta(float(line.split('=', 5)[5].split(' ', 1)[0]))
            time_percent = time_string.total_seconds() / media_duration.total_seconds()
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
    XFER_THREAD = common_xfer.FileSenderThread(row_data['mm_sync_options_json']['TargetIP'],
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
# db_connection.store record in activity table
db_connection.db_commit()
db_connection.db_close()
return
