import natsort
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_metadata_tv = Blueprint('name_blueprint_user_metadata_tv',
                                       url_prefix='/user')


@blueprint_user_metadata_tv.route('/user_meta_tvshow_detail/<guid>')
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_tv_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_detail(request, guid):
    """
    Display metadata of tvshow
    """
    db_connection = await request.app.db_pool.acquire()
    data_metadata = await request.app.db_functions.db_meta_tv_detail(guid,
                                                                     db_connection=db_connection)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'meta tvshow json':
                                                                             data_metadata[
                                                                                 'mm_metadata_tvshow_json']})
    if 'episode_run_time' in data_metadata['mm_metadata_tvshow_json']:
        try:
            data_runtime = data_metadata['mm_metadata_tvshow_json']['episode_run_time'][0]
        except:
            data_runtime = data_metadata['mm_metadata_tvshow_json']['episode_run_time']
    else:
        data_runtime = None
    # TODO there must be sum rating on stuff......
    if 'rating' in data_metadata['mm_metadata_tvshow_json']:
        data_rating = data_metadata['mm_metadata_tvshow_json']['rating']
    else:
        data_rating = None
    if 'first_air_date' in data_metadata['mm_metadata_tvshow_json']:
        data_first_aired = data_metadata['mm_metadata_tvshow_json']['first_air_date']
    else:
        data_first_aired = None
    if 'overview' in data_metadata['mm_metadata_tvshow_json']:
        data_overview = data_metadata['mm_metadata_tvshow_json']['overview']
    else:
        data_overview = None
    # build gen list
    data_genres_list = ''
    if 'genres' in data_metadata['mm_metadata_tvshow_json']:
        for ndx in data_metadata['mm_metadata_tvshow_json']['genres']['name']:
            data_genres_list += (ndx + ', ')
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_metadata['mm_metadata_tvshow_json']['Backdrop'] is not None:
            data_background_image = data_metadata['mm_metadata_tvshow_json']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    data_season_data = await request.app.db_functions.db_meta_tv_eps_season(guid, db_connection)
    #    # build production list
    #    production_list = ''
    #    for ndx in range(0,len(json_metadata['production_companies'])):
    #        production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
    await request.app.db_pool.release(db_connection)
    return {
        'data_title': data_metadata['mm_metadata_tvshow_name'],
        'data_runtime': data_runtime,
        'data_guid': guid,
        'data_rating': data_rating,
        'data_first_aired': data_first_aired,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
        'data_overview': data_overview,
        'data_season_data': data_season_data,
        'data_season_count': sorted(data_season_data),
        'data_genres_list': data_genres_list[:-2],
    }


# tv show season detail - show guid then season #
@blueprint_user_metadata_tv.route("/user_meta_tvshow_episode_detail/<guid>/<eps_id>",
                                  methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_metadata_tv_episode_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_episode_detail(request, guid, eps_id):
    """
    Display tvshow episode metadata detail
    """
    db_connection = await request.app.db_pool.acquire()
    data_metadata = await request.app.db_functions.db_meta_tv_epsisode_by_id(guid, eps_id,
                                                                             db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_metadata['Backdrop'] is not None:
            data_background_image = data_metadata['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return {
        'data': data_metadata[0],
        'data_guid': guid,
        'data_title': data_metadata['eps_name'],
        'data_runtime': data_metadata['eps_runtime'],
        'data_overview=': data_metadata['eps_overview'],
        'data_first_aired': data_metadata['eps_first_air'],
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
    }


@blueprint_user_metadata_tv.route('/user_meta_tvshow_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_tv.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_list(request):
    """
    Display tvshow metadata list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media_tvshow = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_meta_tv_list(offset,
                                                                   int(request.ctx.session[
                                                                           'per_page']),
                                                                   request.ctx.session[
                                                                       'search_text'],
                                                                   db_connection=db_connection):
        media_tvshow.append((row_data['mm_metadata_tvshow_guid'],
                             row_data['mm_metadata_tvshow_name'],
                             row_data['air_date'].replace('"', ''),
                             row_data['image_json']))
    request.ctx.session['search_page'] = 'meta_tv'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_tvshow_list',
                                                                      item_count=await request.app.db_functions.db_meta_tv_list_count(
                                                                          request.ctx.session[
                                                                              'search_text'],
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media_tvshow': media_tvshow,
        'pagination_links': pagination,
    }


# tv show season detail - show guid then season #
@blueprint_user_metadata_tv.route("/user_meta_tvshow_season_detail/<guid>/<season>",
                                  methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_tv_season_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_season_detail(request, guid, season):
    """
    Display metadata of tvshow season detail
    """
    db_connection = await request.app.db_pool.acquire()
    data_metadata = await request.app.db_functions.db_meta_tv_detail(guid,
                                                                     db_connection=db_connection)
    if 'tvmaze' in data_metadata['mm_metadata_tvshow_json']['Meta']:
        if 'runtime' in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']:
            data_runtime = data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']:
            data_rating = data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']['rating'][
                'average']
        else:
            data_rating = None
        if 'premiered' in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']:
            data_first_aired = data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze'][
                'premiered']
        else:
            data_first_aired = None
        if 'summary' in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']:
            data_overview \
                = data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']['summary'].replace(
                '<p>', '').replace('</p>', '')
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'genres' in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']:
            for ndx in data_metadata['mm_metadata_tvshow_json']['Meta']['tvmaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'thetvdb' in data_metadata['mm_metadata_tvshow_json']['Meta']:
        if 'Runtime' in data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta'][
            'Series']:
            data_runtime = \
                data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
                    'Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta'][
            'Series']:
            data_rating = \
                data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
                    'ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta'][
            'Series']:
            data_first_aired = \
                data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
                    'FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta'][
            'Series']:
            data_overview = \
                data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
                    'Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'Genre' in data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'] \
                and data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
            'Genre'] is not None:
            for ndx in \
            data_metadata['mm_metadata_tvshow_json']['Meta']['thetvdb']['Meta']['Series'][
                'Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]
    data_episode_count = await request.app.db_functions.db_meta_tv_season_eps_list(
        guid, int(season), db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'dataeps': data_episode_count})
    data_episode_keys = natsort.natsorted(data_episode_count)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'dataepskeys': data_episode_keys})
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_metadata['mm_metadata_tvshow_json']['Backdrop'] is not None:
            data_background_image = data_metadata['mm_metadata_tvshow_json']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return {
        'data': data_metadata['mm_metadata_tvshow_name'],
        'data_guid': guid,
        'data_season': season,
        'data_overview': data_overview,
        'data_rating': data_rating,
        'data_first_aired': data_first_aired,
        'data_runtime': data_runtime,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
        'data_episode_count': data_episode_count,
        'data_episode_keys': data_episode_keys,
    }
