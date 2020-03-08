from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_media_collection = Blueprint('name_blueprint_user_media_colletion',
                                            url_prefix='/user')


@blueprint_user_media_collection.route('/media_movie_collection', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/media_movie_collection.html')
async def url_bp_user_metadata_movie_collection(request):
    """
    Display movie collection metadata
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    for row_data in g.db_connection.db_collection_list(offset, per_page,
                                                       common_global.session['search_text']):
        if 'Poster' in row_data['mm_metadata_collection_imagelocal_json']:
            media.append((row_data['mm_metadata_collection_guid'],
                          row_data['mm_metadata_collection_name'],
                          row_data['mm_metadata_collection_imagelocal_json']['Poster']))
        else:
            media.append((row_data['mm_metadata_collection_guid'],
                          row_data['mm_metadata_collection_name'], None))
    common_global.session['search_page'] = 'meta_movie_collection'
    pagination = Pagination(request,
                            total=g.db_connection.db_collection_list_count(
                                common_global.session['search_text']),
                            record_name='movie collection(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_media_collection.route('/media_movie_collection_detail/<guid>')
@common_global.jinja_template.template('user/media_movie_collection_detail.html')
async def url_bp_user_metadata_movie_collection_detail(request, guid):
    """
    Display movie collection metadata detail
    """
    data_metadata = g.db_connection.db_collection_read_by_guid(guid)
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
