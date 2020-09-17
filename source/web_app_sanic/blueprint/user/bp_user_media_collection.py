from common import common_global
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_media_collection = Blueprint('name_blueprint_user_media_collection',
                                            url_prefix='/user')


@blueprint_user_media_collection.route('/user_media_movie_collection', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_movie_collection.html')
@common_global.auth.login_required
async def url_bp_user_metadata_movie_collection(request):
    """
    Display movie collection metadata
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_collection_list(offset,
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      request.ctx.session[
                                                                          'search_text'],
                                                                      db_connection):
        if 'Poster' in row_data['mm_metadata_collection_imagelocal_json']:
            media.append((row_data['mm_metadata_collection_guid'],
                          row_data['mm_metadata_collection_name'],
                          row_data['mm_metadata_collection_imagelocal_json']['Poster']))
        else:
            media.append((row_data['mm_metadata_collection_guid'],
                          row_data['mm_metadata_collection_name'], None))
    request.ctx.session['search_page'] = 'meta_movie_collection'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_media_movie_collection',
                                                                      item_count=await request.app.db_functions.db_collection_list_count(
                                                                          db_connection,
                                                                          request.ctx.session[
                                                                              'search_text']),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media,
        'pagination_links': pagination,
    }


@blueprint_user_media_collection.route('/user_media_movie_collection_detail/<guid>')
@common_global.jinja_template.template(
    'bss_user/metadata/bss_user_metadata_movie_collection_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_movie_collection_detail(request, guid):
    """
    Display movie collection metadata detail
    """
    db_connection = await request.app.db_pool.acquire()
    data_metadata = await request.app.db_functions.db_collection_read_by_guid(guid, db_connection)
    await request.app.db_pool.release(db_connection)
    json_metadata = data_metadata['mm_metadata_collection_json']
    json_imagedata = data_metadata['mm_metadata_collection_imagelocal_json']
    # poster image
    try:
        if json_imagedata['Poster'] is not None:
            data_poster_image = json_imagedata['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Backdrop'] is not None:
            data_background_image = json_imagedata['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return {
        'data_name': json_metadata['name'],
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
        'json_metadata': json_metadata,
    }
