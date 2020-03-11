from common import common_global
from sanic import Blueprint

blueprint_user_tv_live = Blueprint('name_blueprint_user_tv_live', url_prefix='/user')


@blueprint_user_tv_live.route("/tv_live/<schedule_date>/<schedule_time>")
@common_global.auth.login_required
async def url_bp_user_livetv(request, schedule_date, schedule_time):
    """
    Display livetv page
    """
    grid_data = '<table style="width:100%" border="2"></tr><th>Station</th><th>Channel</th>'
    for ndx in range(0, 10):
        grid_data += '<th>' + str((int(schedule_time) + (30 * ndx))) + '</th>'
    grid_data += '</tr>'
    channel_data = ""
    md_used = 2
    last_station = ""
    for row_data in g.db_connection.db_tv_schedule_by_date(db_connection, schedule_date):
        if row_data[0] != last_station and last_station is not None:
            grid_data += '<tr><td>' + last_station + '</td><td>' + row_data[1] + '</td>' \
                         + channel_data + '</tr>'
            channel_data = ""
            md_used = 2
            last_station = row_data[0]
        else:
            if last_station is None:
                last_station = row_data[0]
        # 1800 seconds per half hour segment
        next_md = row_data[2]['duration'] // 1800
        if next_md == 0:
            next_md = 1
        if md_used + next_md > 12:
            next_md = 12 - md_used
        if md_used == 12:
            pass
        else:
            audio_html = ""
            if 'audioProperties' in row_data[2]:
                for audio_features in row_data[2]['audioProperties']:
                    if audio_features == "cc":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'caption-icon.png" alt="Closed Caption"' \
                                      ' style="width:15px;height:15px;">'
                    elif audio_features == "stereo":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'audio_channels/2.png" alt="Stereo Sound"' \
                                      ' style="width:15px;height:15px;">'
                    elif audio_features == "DD 5.1":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'audio_channels/6.png" alt="DD 5.1" style="width:15px;height:15px;">'
                    elif audio_features == "SAP":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'sap-icon.png" alt="SAP" style="width:15px;height:15px;">'
                    elif audio_features == "dvs":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'dvs-icon.png" alt="Descriptive Video Service"' \
                                      ' style="width:15px;height:15px;">'
                    elif audio_features == "DD":
                        audio_html += '<img src="/static/images/media_flags/' \
                                      'audio_codec/dolby_digital.png" alt="Dolby Digital"' \
                                      ' style="width:15px;height:15px;">'
            # TODO
            #    Atmos - Dolby Atmos
            #    Dolby
            #    dubbed
            #    subtitled
            #    surround

            video_html = ""
            if 'videoProperties' in row_data[2]:
                for video_features in row_data[2]['videoProperties']:
                    if video_features == "3d":
                        video_html += '<img src="/static/images/3D.png" alt="3D"' \
                                      ' style="width:15px;height:15px;">'
                    elif video_features == "hdtv":
                        video_html += '<img src="/static/images/media_flags/' \
                                      'video_resolution.png" alt="HDTV" style="width:15px;height:15px;">'
            # TODO
            #    enhanced - Enhanced is better video quality than Standard Definition,
            # but not true High Definition. (720p / 1080i)
            #    letterbox
            #    sdtv
            #    uhdtv - the content is in "UHDTV"; this is provider-dependent and does not imply
            # any particular resolution or encoding

            rating_html = ""
            if 'ratings' in row_data[2]:
                for rating_features in row_data[2]['ratings']:
                    if rating_features['code'] == "TVG":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-G.png" alt="TV-G" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY7":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-Y7.png" alt="TV-Y7" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVY":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-Y.png" alt="TV-Y" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVPG":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-PG.png" alt="TV-PG" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TV14":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-14.png" alt="TV-14" style="width:15px;height:15px;">'
                    elif rating_features['code'] == "TVMA":
                        rating_html += '<img src="/static/images/media_flags/' \
                                       'content_rating/TV-MA.png" alt="TV-MA" style="width:15px;height:15px;">'
            channel_data += '<td colspan="' + str(next_md) + '\">' + row_data[2]['programID'] \
                            + audio_html + rating_html + '</td>'
            md_used += next_md
    # populate last row
    grid_data += '<tr><td>' + last_station + '</td>' + channel_data + '</tr>'
    return render_template("users/user_livetv_page.html", media=grid_data)


@blueprint_user_tv_live.route("/tv_live_detail/<guid>")
@common_global.auth.login_required
async def url_bp_user_tv_live_detail(request, guid):
    """
    Display live tv detail page
    """
    return render_template("users/user_tv_live.html")
