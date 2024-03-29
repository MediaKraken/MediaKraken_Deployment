from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_metadata_music = Blueprint('name_blueprint_user_metadata_music', url_prefix='/user')


@blueprint_user_metadata_music.route('/user_meta_music_album_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_music_album.html')
@common_global.auth.login_required
async def url_bp_user_metadata_music_album_list(request):
    """
    Display metadata of album list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for album_data in await request.app.db_functions.db_meta_music_album_list(offset,
                                                                              int(
                                                                                  request.ctx.session[
                                                                                      'per_page']),
                                                                              request.ctx.session[
                                                                                  'search_text'],
                                                                              db_connection=db_connection):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'album_data': album_data,
                                                                             'id': album_data[
                                                                                 'mm_metadata_album_guid'],
                                                                             'name': album_data[
                                                                                 'mm_metadata_album_name'],
                                                                             'json': album_data[
                                                                                 'mm_metadata_album_json']})
        if album_data['mmp_person_image'] is not None:
            if 'musicbrainz' in album_data['mm_metadata_album_image']['Images']:
                try:
                    album_image = album_data['mm_metadata_album_image']['Images']['musicbrainz']
                except:
                    album_image = "img/music_album_missing.png"
            else:
                album_image = "img/music_album_missing.png"
        else:
            album_image = "img/music_album_missing.png"
            media.append(
                (album_data['mm_metadata_album_guid'], album_data['mm_metadata_album_name'],
                 album_image))
    request.ctx.session['search_page'] = 'meta_album'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_music_album_list',
                                                                      item_count=await request.app.db_functions.db_table_count(
                                                                          table_name='mm_metadata_album',
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media,
        'pagination_links': pagination,
    }


@blueprint_user_metadata_music.route('/user_meta_music_album_song_list', methods=['GET', 'POST'])
@common_global.jinja_template.template(
    'bss_user/metadata/bss_user_metadata_music_album_detail.html')
@common_global.auth.login_required
async def metadata_music_album_song_list(request):
    """
    Display metadata music song list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    request.ctx.session['search_page'] = 'meta_music_song'
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_music_album_song_list',
                                                                      item_count=await request.app.db_functions.db_table_count(
                                                                          table_name='mm_metadata_music',
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_data = await request.app.db_functions.db_meta_music_song_list(offset,
                                                                        int(request.ctx.session[
                                                                                'per_page']),
                                                                        request.ctx.session[
                                                                            'search_text'],
                                                                        db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }
