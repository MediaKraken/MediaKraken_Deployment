import json

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
    json_metadata = json.loads(data_metadata['mm_metadata_tvshow_json'])
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'meta tvshow json': json_metadata})
    if 'episode_run_time' in json_metadata:
        try:
            data_runtime = json_metadata['episode_run_time'][0]
        except:
            data_runtime = json_metadata['episode_run_time']
    else:
        data_runtime = None
    # TODO there must be sum rating on stuff......
    if 'rating' in json_metadata:
        data_rating = json_metadata['rating']
    else:
        data_rating = None
    if 'first_air_date' in json_metadata:
        data_first_aired = json_metadata['first_air_date']
    else:
        data_first_aired = None
    if 'overview' in json_metadata:
        data_overview = json_metadata['overview']
    else:
        data_overview = None
    # build gen list
    data_genres_list = ''
    if 'genres' in json_metadata:
        for ndx in json_metadata['genres']['name']:
            data_genres_list += (ndx + ', ')
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['Backdrop'] is not None:
            data_background_image = json_metadata['Backdrop']
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
                             json.loads(row_data['image_json'])))
    request.ctx.session['search_page'] = 'meta_tv'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_tvshow_list',
                                                                      item_count=await request.app.db_functions.db_meta_tv_list_count(
                                                                          db_connection=db_connection,
                                                                          request.ctx.session[
                                                                              'search_text']),
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
    data_metadata = await request.app.db_functions.db_meta_tv_detail(guid, db_connection=db_connection)
    json_metadata = json.loads(data_metadata['mm_metadata_tvshow_json'])
    if 'tvmaze' in json_metadata['Meta']:
        if 'runtime' in json_metadata['Meta']['tvmaze']:
            data_runtime = json_metadata['Meta']['tvmaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in json_metadata['Meta']['tvmaze']:
            data_rating = json_metadata['Meta']['tvmaze']['rating']['average']
        else:
            data_rating = None
        if 'premiered' in json_metadata['Meta']['tvmaze']:
            data_first_aired = json_metadata['Meta']['tvmaze']['premiered']
        else:
            data_first_aired = None
        if 'summary' in json_metadata['Meta']['tvmaze']:
            data_overview \
                = json_metadata['Meta']['tvmaze']['summary'].replace('<p>', '').replace('</p>', '')
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'genres' in json_metadata['Meta']['tvmaze']:
            for ndx in json_metadata['Meta']['tvmaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'thetvdb' in json_metadata['Meta']:
        if 'Runtime' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_runtime = json_metadata['Meta']['thetvdb']['Meta']['Series']['Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_rating = json_metadata['Meta']['thetvdb']['Meta']['Series']['ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_first_aired = json_metadata['Meta']['thetvdb']['Meta']['Series']['FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_overview = json_metadata['Meta']['thetvdb']['Meta']['Series']['Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'Genre' in json_metadata['Meta']['thetvdb']['Meta']['Series'] \
                and json_metadata['Meta']['thetvdb']['Meta']['Series']['Genre'] is not None:
            for ndx in json_metadata['Meta']['thetvdb']['Meta']['Series']['Genre'].split("|"):
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
        if json_metadata['Backdrop'] is not None:
            data_background_image = json_metadata['Backdrop']
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
