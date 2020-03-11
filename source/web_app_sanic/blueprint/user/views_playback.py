

@blueprint.route('/playalbum/<guid>')
@login_required
async def url_bp_user_album_player(request, guid):
    """
    Obsolete?
    """
    return render_template("users/user_album_playback.html",
                           data_desc=await request.app.db_functions.db_meta_album_by_guid(db_connection,
                               guid),
                           data_song_list=await request.app.db_functions.db_meta_songs_by_album_guid(db_connection, guid))


@blueprint.route('/playvideo_videojs/<mtype>/<guid>/<chapter>/<audio>/<sub>', methods=['GET',
                                                                                       'POST'])
@login_required
async def url_bp_user_video_player_videojs(request, mtype, guid, chapter, audio, sub):
    """
    Display video playback page
    """
    # TODO will need start time/etc for resume function
    common_global.es_inst.com_elastic_index('info',
                                            {"videojs": mtype, 'guid': guid, 'chapter': chapter,
                                             'audio': audio, 'sub': sub})
    # grab the guid from the comboindex
    media_path = await request.app.db_functions.db_media_path_by_uuid(db_connection, guid)
    # set ffpmeg options with the play_data
    atracks = '-map ' + audio
    if sub is not None:
        subtracks = 'subtitles=\"' + media_path + '\" language=' + sub
    else:
        subtracks = ''
    # fire up ffmpeg process
    if mtype == "hls":
        # must be done here so can send commands for the right stream
        target_uuid = str(uuid.uuid4())
        vid_name = "./static/cache/" + target_uuid + ".m3u8"

        # ffmpeg -i input.mp4 -profile:v baseline -level 3.0 -s 640x360
        # -start_number 0 -hls_time 10 -hls_list_size 0 -f hls index.m3u8

        common_network_pika.com_net_pika_send({'Type': 'Play', 'Subtype': 'HLS',
                                               'Input File': media_path,
                                               'Audio Track': atracks,
                                               'Subtitle Track': subtracks,
                                               'Target UUID': target_uuid,
                                               'User': user.id},
                                              rabbit_host_name='mkstack_rabbitmq',
                                              exchange_name='mkque_ex',
                                              route_key='mkque')
        # TODO how to know what to return here.....slave could be anywhere on swarm
        pass_guid = 'https://th-mediakraken-1' + '/' + vid_name
        # pass_guid = '//s3.amazonaws.com/_bc_dml/example-content/tears-of-steel/playlist.m3u8'
    else:
        pass_guid = guid
        common_global.es_inst.com_elastic_index('info', {"hls path": pass_guid})
    return render_template("users/user_playback_videojs.html",
                           data_desc='Movie title',
                           data_guid=pass_guid,
                           data_mtype=mtype)


@blueprint.route('/playback/<action>/<guid>', methods=['GET', 'POST'])
@login_required
async def url_bp_user_playback(request, action, guid):
    """
    Display actions page
    """
    common_global.es_inst.com_elastic_index('info', {'user_playback action': action,
                                                     'case user': user.id})
    # pull the media stats
    common_global.es_inst.com_elastic_index('info', {'args': request.args})
    common_global.es_inst.com_elastic_index('info', {'form': request.form})
    request_id = request.form['id']
    audio_track = request.form['audio|%s' % request_id]
    subtitle_track = request.form['subtitle|%s' % request_id]
    playback_device = request.form['playback_device|%s' % request_id]

    if action == 'base':
        pass
    elif action == 'back':
        pass
    #    elif action == 'rewind':
    #        pass
    elif action == 'stop':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Stop', 'Device': device,
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'play':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Play', 'Device': device,
             'User': user.id,
             'Data': await request.app.db_functions.db_read_media(db_connection, guid)['mm_media_path'],
             'Audio': audio_track,
             'Subtitle': subtitle_track,
             'Target': playback_device},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'pause':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Pause', 'Device': device,
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'forward':
        pass
    elif action == 'mute':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Mute', 'Device': device,
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol_up':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Up', 'Device': device,
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol down':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Down', 'Device': device,
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    return render_template("users/user_playback.html")

