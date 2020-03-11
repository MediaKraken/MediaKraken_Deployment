from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_music = Blueprint('name_blueprint_user_metadata_music', url_prefix='/user')


@blueprint_user_metadata_music.route('/meta_music_album_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_music_album_list.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_album_list(request):
    """
    Display metadata of album list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    for album_data in await request.app.db_functions.db_meta_album_list(db_connection, offset, per_page,
                                                         request['session']['search_text']):
        common_global.es_inst.com_elastic_index('info', {'album_data': album_data,
                                                         'id': album_data['mm_metadata_album_guid'],
                                                         'name': album_data[
                                                             'mm_metadata_album_name'],
                                                         'json': album_data[
                                                             'mm_metadata_album_json']})
        if album_data['mmp_person_image'] is not None:
            if 'musicbrainz' in album_data['mm_metadata_album_image']['Images']:
                try:
                    album_image = album_data['mm_metadata_album_image']['Images'][
                        'musicbrainz'].replace(
                        '/mediakraken/web_app/MediaKraken', '')
                except:
                    album_image = "/static/images/music_album_missing.png"
            else:
                album_image = "/static/images/music_album_missing.png"
        else:
            album_image = "/static/images/music_album_missing.png"
            media.append(
                (album_data['mm_metadata_album_guid'], album_data['mm_metadata_album_name'],
                 album_image))
    request['session']['search_page'] = 'meta_album'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                'mm_metadata_album'),
                            record_name='album(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_metadata_music.route('/meta_music_album_song_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_music_album_song_list.html')
@common_global.auth.login_required
async def metadata_music_album_song_list(request):
    """
    Display metadata music song list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    request['session']['search_page'] = 'meta_music_song'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                'mm_metadata_music'),
                            record_name='song(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': await request.app.db_functions.db_meta_song_list(db_connection, offset, per_page,
                                                   request['session']['search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
