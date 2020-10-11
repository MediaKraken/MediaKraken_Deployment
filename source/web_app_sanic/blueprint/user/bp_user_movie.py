import json
import subprocess
from shlex import split

from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch_httpx
from common import common_network_pika
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_movie = Blueprint('name_blueprint_user_movie', url_prefix='/user')


@blueprint_user_movie.route('/user_movie_detail/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_movie_detail.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_movie_detail(request, user, guid):
    """
    Display move detail page
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_pool.set_type_codec('json',
                                             encoder=json.dumps,
                                             decoder=json.loads,
                                             schema='pg_catalog')
    if request.method == 'POST':
        if request.form['playback'] == 'Web Viewer':
            common_network_pika.com_net_pika_send(
                {'Type': 'Playback', 'Subtype': 'Play', 'Device': 'Web',
                 'User': user.id,
                 'Data': await
                 request.app.db_functions.db_read_media(guid, db_connection=db_connection)[
                     'mm_media_path']},
                rabbit_host_name='mkstack_rabbitmq',
                exchange_name='mkque_ex',
                route_key='mkque')
            return redirect(
                request.app.url_for('name_blueprint_user_playback_video.user_video_player_videojs',
                                    mtype='hls',
                                    guid=request.form['Video_Track'], chapter=1,
                                    audio=request.form['Video_Play_Audio_Track'],
                                    sub=request.form['Video_Play_Subtitles']))
        if request.form['status'] == 'Watched':
            await request.app.db_functions.db_meta_movie_status_update(guid, user.id, False,
                                                                       db_connection=db_connection)
            return redirect(
                request.app.url_for('name_blueprint_user_movie.url_bp_user_movie_detail',
                                    guid=guid))
        elif request.form['status'] == 'Unwatched':
            await request.app.db_functions.db_meta_movie_status_update(guid, user.id, True,
                                                                       db_connection=db_connection)
            return redirect(
                request.app.url_for('name_blueprint_user_movie.url_bp_user_movie_detail',
                                    guid=guid))
        elif request.form['status'] == 'Sync':
            return redirect(
                request.app.url_for('name_blueprint_user_sync.url_bp_user_sync_edit', guid=guid))
        elif request.form['status'] == 'Cast':
            # TODO submit cast comment via rabbitmq
            # grab the guid from the comboindex
            media_guid_index = request.form["Video_Track"]
            # call ffpmeg with the play_data
            audio_track_index = request.form["Video_Play_Audio_Track"]
            subtitle_track_index = request.form["Video_Play_Subtitles"]
            # launch ffmpeg to ffserver procecss
            # TODO fire up node cast container!
            proc_ffserver = subprocess.Popen(split('ffmpeg  -i \"',
                                                   await
                                                   request.app.db_functions.db_media_path_by_uuid(
                                                       media_guid_index,
                                                       db_connection=db_connection)[
                                                       0] + '\" http://localhost/stream.ffm'),
                                             stdout=subprocess.PIPE, shell=False)
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "FFServer PID": proc_ffserver.pid})
            return redirect(
                request.app.url_for('name_blueprint_user_movie.url_bp_user_movie_detail',
                                    guid=guid))
    else:
        metadata_data = await request.app.db_functions.db_meta_movie_by_media_uuid(guid,
                                                                                   db_connection=db_connection)
        # poster image
        try:
            # don't bother checking for NONE as that's valid
            data_poster_image = metadata_data['mm_metadata_localimage_json']['Poster']
        except:
            data_poster_image = None
        # background image
        try:
            # don't bother checking for NONE as that's valid
            data_background_image = metadata_data['mm_metadata_localimage_json']['Backdrop']
        except:
            data_background_image = None

        # build gen list
        genres_list = []
        for ndx in range(0, len(metadata_data['mm_metadata_json']['genres'])):
            genres_list.append(metadata_data['mm_metadata_json']['genres'][ndx]['name'])

        # not sure if the following with display anymore
        # # vote count format
        # data_vote_count = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['vote_count'])
        # # build production list
        # production_list = ''
        # for ndx in range(0,
        #                  len(metadata_data['mm_metadata_json']['production_companies'])):
        #     production_list \
        #         += (metadata_data['mm_metadata_json']['production_companies'][ndx]['name']
        #             + ', ')
        # # budget format
        # budget = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['budget'])
        # # revenue format
        # revenue = common_internationalization.com_inter_number_format(
        #     metadata_data['mm_metadata_json']['revenue'])
        # # grab reviews
        # review = []
        # review_json = await request.app.db_functions.db_review_list_by_tmdb_guid(json_metaid['themoviedb'], db_connection)
        # if review_json is not None and len(review_json) > 0:
        #     review_json = review_json[0]
        #     for review_data in review_json[1]['themoviedb']['results']:
        #         review.append(
        #             (review_data['author'], review_data['url'], review_data['content']))
        # # set watched and sync
        # try:
        #     watched_status = json_media['UserStats'][user.id]['Watched']
        # except:
        #     watched_status = False
        # try:
        #     sync_status = json_media['Synced']
        # except:
        #     sync_status = False

        # check to see if there are other version(s) of this video file (dvd, hddvd, etc)
        ffprobe_data = {}
        # TODO  the following does alot of repeats sumhow.   due to dict it stomps over itself
        for video_version in await request.app.db_functions.db_media_ffprobe_all_guid(guid,
                                                                                      common_global.DLMediaType.Movie.value,
                                                                                      db_connection=db_connection):
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 "vid_version": video_version})
            # not all files have ffprobe
            if video_version['mm_media_ffprobe_json'] is None:
                hours = 0
                minutes = 0
                seconds = 0
                data_resolution = "NA"
            else:
                # calculate a better runtime instead of just seconds
                try:
                    minutes, seconds = divmod(
                        float(video_version['mm_media_ffprobe_json']['format']['duration']), 60)
                    hours, minutes = divmod(minutes, 60)
                except:
                    hours = 0
                    minutes = 0
                    seconds = 0
                # TODO will need to be able to loop through streams...for those with multiple videos in container
                try:
                    data_resolution = str(
                        video_version['mm_media_ffprobe_json']['streams'][0]['width']) + 'x' \
                                      + str(
                        video_version['mm_media_ffprobe_json']['streams'][0]['height'])
                except:
                    data_resolution = 'NA'
            # audio and sub streams
            audio_streams = []
            subtitle_streams = []
            if video_version['mm_media_ffprobe_json'] is not None:
                for stream_info in video_version['mm_media_ffprobe_json']['streams']:
                    if stream_info['codec_type'] == 'audio':
                        try:
                            stream_language = common_internationalization.com_inter_country_name(
                                stream_info['tags']['language'])  # eng, spa and so on
                        except KeyError:
                            stream_language = 'NA'
                        try:
                            stream_title = stream_info['tags']['title']  # Surround 5.1 and so on
                        except KeyError:
                            stream_title = 'NA'
                        if 'codec_long_name' in stream_info and stream_info[
                            'codec_long_name'] != 'unknown':
                            stream_codec = stream_info['codec_long_name']
                        else:
                            try:
                                stream_codec = stream_info['codec_name']
                            except KeyError:
                                stream_codec = 'NA'
                        audio_streams.append((stream_codec, stream_language, stream_title))
                    elif stream_info['codec_type'] == 'subtitle':
                        try:
                            subtitle_streams.append(
                                common_internationalization.com_inter_country_name(
                                    stream_info['tags']['language']))
                        except KeyError:
                            subtitle_streams.append('Unknown')
            ffprobe_data[video_version['mm_media_guid']] = (data_resolution,
                                                            "%02dH:%02dM:%02dS" % (
                                                                hours, minutes, seconds),
                                                            audio_streams,
                                                            subtitle_streams)
        # do chapter stuff here so I can sort
        data_json_media_chapters = []
        # try:
        #     for chap_data in natsort.natsorted(json_media['ChapterImages']):
        #         data_json_media_chapters.append((chap_data,
        #                                          json_media['ChapterImages'][chap_data]))
        # except:
        #     pass

        # find all devices to playback media on
        # TODO have reactor return client list?
        playback_devices = []
        for device_item in await request.app.db_functions.db_device_list(
                db_connection=db_connection):
            if device_item['mm_device_type'] == 'Chromecast':
                playback_devices.append(device_item['mm_device_json']['Name'])
            elif device_item['mm_device_type'] == 'Roku':
                playback_devices.append(device_item)

        await request.app.db_pool.release(db_connection)
        return {
            'json_metadata': metadata_data,
            'data_genres': genres_list,
            'data_poster_image': data_poster_image,
            'data_background_image': data_background_image,
            'data_json_media_chapters': data_json_media_chapters,
            'data_ffprobe_data': ffprobe_data,
            'data_playback_device': playback_devices,
            # data_watched_status=watched_status,
            # data_sync_status=sync_status
        }
    await request.app.db_pool.release(db_connection)
