from common import common_global
from common import common_internationalization
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_movie = Blueprint('name_blueprint_user_metadata_movie',
                                          url_prefix='/user')


@blueprint_user_metadata_movie.route('/meta_movie_detail/<guid>')
@common_global.jinja_template.template('user/meta_movie_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_movie_detail(request, guid):
    """
    Display metadata movie detail
    """
    db_connection = await request.app.db_pool.acquire()
    data = await request.app.db_functions.db_read_media_metadata(db_connection, guid)
    json_metadata = data['mm_metadata_json']
    json_imagedata = data['mm_metadata_localimage_json']
    # vote count format
    data_vote_count = common_internationalization.com_inter_number_format(
        json_metadata['Meta']['themoviedb']['Meta']['vote_count'])
    # build gen list
    genres_list = ''
    for ndx in range(0, len(json_metadata['Meta']['themoviedb']['Meta']['genres'])):
        genres_list += (json_metadata['Meta']['themoviedb']
                        ['Meta']['genres'][ndx]['name'] + ', ')
    # build production list
    production_list = ''
    for ndx in range(0, len(json_metadata['Meta']['themoviedb']['Meta']['production_companies'])):
        production_list \
            += (json_metadata['Meta']['themoviedb']['Meta']['production_companies'][ndx]['name']
                + ', ')
    # poster image
    try:
        if json_imagedata['Images']['themoviedb']['Poster'] is not None:
            data_poster_image \
                = json_imagedata['Images']['themoviedb']['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Images']['themoviedb']['Backdrop'] is not None:
            data_background_image = json_imagedata['Images']['themoviedb']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    # grab reviews
    review = await request.app.db_functions.db_review_list_by_tmdb_guid(db_connection, data[1])
    await request.app.db_pool.release(db_connection)
    return {
        # data_media_ids: data[1],
        'data_name': data[2],
        'json_metadata': json_metadata,
        'data_genres': genres_list[:-2],
        'data_production': production_list[:-2],
        # data_review: review,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
        'data_vote_count': data_vote_count,
        'data_budget': common_internationalization.com_inter_number_format(
            json_metadata['Meta']['themoviedb']['Meta']['budget'])
    }


@blueprint_user_metadata_movie.route('/meta_movie_list', methods=["GET", "POST"])
@common_global.jinja_template.template('user/meta_movie_list.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_metadata_movie_list(request, user):
    """
    Display list of movie metadata
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    media_count = 0
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_meta_movie_list(db_connection, offset, per_page,
                                                       request['session']['search_text']):
        # set watched
        try:
            watched_status \
                = row_data['mm_metadata_user_json']['UserStats'][user.id]['watched']
        except (KeyError, TypeError):
            watched_status = False
        # set rating
        if row_data['mm_metadata_user_json'] is not None \
                and 'UserStats' in row_data['mm_metadata_user_json'] \
                and user.id in row_data['mm_metadata_user_json']['UserStats'] \
                and 'Rating' in row_data['mm_metadata_user_json']['UserStats'][
            user.id]:
            rating_status \
                = row_data['mm_metadata_user_json']['UserStats'][user.id]['Rating']
            if rating_status == 'favorite':
                rating_status = '/static/images/favorite-mark.png'
            elif rating_status == 'like':
                rating_status = '/static/images/thumbs-up.png'
            elif rating_status == 'dislike':
                rating_status = '/static/images/dislike-thumb.png'
            elif rating_status == 'poo':
                rating_status = '/static/images/pile-of-dung.png'
        else:
            rating_status = None
        # set requested
        try:
            request_status \
                = row_data['mm_metadata_user_json']['UserStats'][user.id]['requested']
        except (KeyError, TypeError):
            request_status = None
        # set queue
        try:
            queue_status \
                = row_data['mm_metadata_user_json']['UserStats'][user.id]['queue']
        except (KeyError, TypeError):
            queue_status = None
        common_global.es_inst.com_elastic_index('info', {"status": watched_status,
                                                         'rating': rating_status,
                                                         'request': request_status,
                                                         'queue': queue_status})
        media_count += 1
        if media_count == 1:
            deck_start = True
        else:
            deck_start = False
        if media_count == 4:
            deck_break = True
            media_count = 0
        else:
            deck_break = False
        media.append((row_data['mm_metadata_guid'], row_data['mm_media_name'],
                      row_data['mm_date'], row_data['mm_poster'], watched_status,
                      rating_status, request_status, queue_status, deck_start, deck_break))
    request['session']['search_page'] = 'meta_movie'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_movie_count(db_connection,
                                request['session']['search_text']),
                            record_name='movie(s)',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {
        'media_movie': media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
