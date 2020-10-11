from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch_httpx
from common import common_pagination_bootstrap
from sanic import Blueprint, response

blueprint_user_metadata_movie = Blueprint('name_blueprint_user_metadata_movie',
                                          url_prefix='/user')


@blueprint_user_metadata_movie.route('/user_meta_movie_detail/<guid>')
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_movie_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_movie_detail(request, guid):
    """
    Display metadata movie detail
    """
    db_connection = await request.app.db_pool.acquire()
    data = await request.app.db_functions.db_meta_movie_detail(media_guid=guid,
                                                               db_connection=db_connection)
    # vote count format
    try:
        data_vote_count = common_internationalization.com_inter_number_format(
            data['mm_metadata_json']['vote_count'])
    except:
        data_vote_count = 'NA'
    # build gen list
    genres_list = ''
    for ndx in range(0, len(data['mm_metadata_json']['genres'])):
        genres_list += (data['mm_metadata_json']['genres'][ndx]['name'] + ', ')
    # build production list
    production_list = ''
    for ndx in range(0, len(data['mm_metadata_json']['production_companies'])):
        production_list \
            += (data['mm_metadata_json']['production_companies'][ndx]['name'] + ', ')
    # poster image
    try:
        if data['mm_metadata_localimage_json']['Poster'] is not None:
            data_poster_image = data['mm_metadata_localimage_json']['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if data['mm_metadata_localimage_json']['Backdrop'] is not None:
            data_background_image = data['mm_metadata_localimage_json']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    # grab reviews
    review = await request.app.db_functions.db_review_list_by_meta_guid(metadata_id=guid,
                                                                        db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'data_name': data['mm_media_name'],
        'json_metadata': data['mm_metadata_json'],
        'data_genres': genres_list[:-2],
        'data_production': production_list[:-2],
        'data_review': review,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
        'data_vote_count': data_vote_count,
        'data_budget': common_internationalization.com_inter_number_format(
            data['mm_metadata_json']['budget'])
    }


@blueprint_user_metadata_movie.route('/user_meta_movie_list', methods=["GET", "POST"])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_movie.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_metadata_movie_list(request, user):
    """
    Display list of movie metadata
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media = []
    media_count = 0
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_meta_movie_list(offset,
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      request.ctx.session[
                                                                          'search_text'],
                                                                      db_connection):
        if row_data['mm_metadata_user_json'] is not None:
            user_json = row_data['mm_metadata_user_json']
        else:
            user_json = None
        # set watched
        try:
            watched_status = user_json['UserStats'][str(user.id)]['watched']
        except (KeyError, TypeError):
            watched_status = False
        # set rating
        if user_json is not None \
                and 'UserStats' in user_json \
                and str(user.id) in user_json['UserStats'] \
                and 'Rating' in user_json['UserStats'][str(user.id)]:
            rating_status \
                = user_json['UserStats'][str(user.id)]['Rating']
            if rating_status == 'favorite':
                rating_status = 'favorite-mark.png'
            elif rating_status == 'like':
                rating_status = 'thumbs-up.png'
            elif rating_status == 'dislike':
                rating_status = 'dislike-thumb.png'
            elif rating_status == 'poo':
                rating_status = 'pile-of-dung.png'
        else:
            rating_status = None
        # set requested
        try:
            request_status = user_json['UserStats'][str(user.id)]['requested']
        except (KeyError, TypeError):
            request_status = None
        # set queue
        try:
            queue_status = user_json['UserStats'][str(user.id)]['queue']
        except (KeyError, TypeError):
            queue_status = None
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             "status": watched_status,
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
                      row_data['mm_date'], row_data['mm_poster'].replace('"', ''), watched_status,
                      rating_status, request_status, queue_status, deck_start, deck_break))
    request.ctx.session['search_page'] = 'meta_movie'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page=page,
                                                                      url='/user/user_meta_movie_list',
                                                                      item_count=await request.app.db_functions.db_meta_movie_count(
                                                                          request.ctx.session[
                                                                              'search_text'],
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media_movie': media,
        'pagination_links': pagination,
    }


@blueprint_user_metadata_movie.route('/user_meta_movie_status/<guid>/<event_type>',
                                     methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_metadata_movie_status(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'movie metadata status': guid,
                                                                         'event': event_type})
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_meta_movie_status_update(guid,
                                                               user.id, event_type,
                                                               db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return response.HTTPResponse('', status=200, headers={'Vary': 'Accept-Encoding'})
