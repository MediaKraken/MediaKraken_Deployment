from common import common_global
from common import common_internationalization
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_media_genre = Blueprint('name_blueprint_user_media_genre', url_prefix='/user')


@blueprint_user_media_genre.route("/media_genre", methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_media_genre.html')
@common_global.auth.login_required
async def url_bp_user_media_genre(request):
    """
    Display media split up by genre
    """
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_media_movie_count_by_genre(db_connection,
            common_global.DLMediaType.Movie.value):
        media.append((row_data['gen']['name'],
                      common_internationalization.com_inter_number_format(
                          row_data[1]),
                      row_data[0]['name'] + ".png"))
    return {
        'media': sorted(media)
    }


@blueprint_user_media_genre.route("/movie/<genre>", methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_movie.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_movie_page(request, user, genre):
    """
    Display movie page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_web_media_list(db_connection,
            common_global.DLMediaType.Movie.value,
            list_type='movie', list_genre=genre, list_limit=per_page, group_collection=False,
            offset=offset, include_remote=True, search_text=request['session']['search_text']):
        # 0- mm_media_name, 1- mm_media_guid, 2- mm_metadata_user_json,
        # 3 - mm_metadata_localimage_json
        common_global.es_inst.com_elastic_index('info',
                                                {"row2": row_data['mm_metadata_user_json']})
        json_image = row_data['mm_metadata_localimage_json']
        # set watched
        try:
            watched_status \
                = row_data['mm_metadata_user_json']['UserStats'][user.id]['watched']
        except (KeyError, TypeError):
            watched_status = False
        # set synced
        try:
            sync_status = \
                row_data['mm_metadata_user_json']['UserStats'][user.id]['sync']
        except (KeyError, TypeError):
            sync_status = False
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
        # set mismatch
        try:
            match_status = row_data['mismatch']
        except (KeyError, TypeError):
            match_status = False
        common_global.es_inst.com_elastic_index('info', {"status": watched_status,
                                                         'sync': sync_status,
                                                         'rating': rating_status,
                                                         'match': match_status})
        if 'themoviedb' in json_image['Images'] and 'Poster' in json_image['Images']['themoviedb'] \
                and json_image['Images']['themoviedb']['Poster'] is not None:
            media.append((row_data['mm_media_name'], row_data['mm_media_guid'],
                          json_image['Images']['themoviedb']['Poster'],
                          watched_status, sync_status, rating_status, match_status))
        else:
            media.append((row_data['mm_media_name'], row_data['mm_media_guid'], None,
                          watched_status, sync_status, rating_status, match_status))
    total = await request.app.db_functions.db_web_media_list_count(db_connection,
        common_global.DLMediaType.Movie.value, list_type='movie', list_genre=genre,
        group_collection=False, include_remote=True, search_text=request['session']['search_text'])
    await request.app.db_pool.release(db_connection)
    request['session']['search_page'] = 'media_movie'
    pagination = Pagination(request,
                            total=total,
                            record_name='movie(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
