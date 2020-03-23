from common import common_global
from sanic import Blueprint

blueprint_user_playback_audio = Blueprint('name_blueprint_user_playback_audio', url_prefix='/user')


@blueprint_user_playback_audio.route('/play_album/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/bss_user_album_playback.html')
@common_global.auth.login_required
async def url_bp_user_playback_album(request, guid):
    """
    Obsolete?
    """
    db_connection = await request.app.db_pool.acquire()
    data_desc = await request.app.db_functions.db_meta_music_album_by_guid(db_connection,
                                                                           guid)
    data_song_list = await request.app.db_functions.db_meta_music_songs_by_album_guid(db_connection,
                                                                                      guid)
    await request.app.db_pool.release(db_connection)
    return {
        data_desc: data_desc,
        data_song_list: data_song_list,
    }
