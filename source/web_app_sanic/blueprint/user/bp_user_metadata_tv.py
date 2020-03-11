import natsort
from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_tv = Blueprint('name_blueprint_user_metadata_tv',
                                       url_prefix='/user')


@blueprint_user_metadata_tv.route('/meta_tvshow_detail/<guid>')
@common_global.jinja_template.template('user/meta_tvshow_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_detail(request, guid):
    """
    Display metadata of tvshow
    """
    data_metadata = await request.app.db_functions.db_meta_tvshow_detail(db_connection, guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    common_global.es_inst.com_elastic_index('info', {'meta tvshow json': json_metadata})
    if 'themoviedb' in json_metadata['Meta']:
        if 'episode_run_time' in json_metadata['Meta']['themoviedb']:
            try:
                data_runtime = json_metadata['Meta']['themoviedb']['episode_run_time'][0]
            except:
                data_runtime = json_metadata['Meta']['themoviedb']['episode_run_time']
        else:
            data_runtime = None
        # TODO there must be sum rating on stuff......
        if 'rating' in json_metadata['Meta']['themoviedb']:
            data_rating = json_metadata['Meta']['themoviedb']['rating']
        else:
            data_rating = None
        if 'first_air_date' in json_metadata['Meta']['themoviedb']:
            data_first_aired = json_metadata['Meta']['themoviedb']['first_air_date']
        else:
            data_first_aired = None
        if 'overview' in json_metadata['Meta']['themoviedb']:
            data_overview = json_metadata['Meta']['themoviedb']['overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'genres' in json_metadata['Meta']['themoviedb']:
            for ndx in json_metadata['Meta']['themoviedb']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'tvmaze' in json_metadata['Meta']:
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
            data_overview = json_metadata['Meta']['tvmaze']['summary']
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
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    data_season_data = await request.app.db_functions.db_read_tvmeta_eps_season(db_connection, guid)
    #    # build production list
    #    production_list = ''
    #    for ndx in range(0,len(json_metadata['production_companies'])):
    #        production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
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
@blueprint_user_metadata_tv.route("/meta_tvshow_episode_detail/<guid>/<eps_id>",
                                  methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_tvshow_episode_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_episode_detail_page(request, guid, eps_id):
    """
    Display tvshow episode metadata detail
    """
    data_metadata = await request.app.db_functions.db_read_tvmeta_epsisode_by_id(db_connection, guid, eps_id)
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = data_metadata['LocalImages']['Backdrop']
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


@blueprint_user_metadata_tv.route('/meta_tvshow_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_tvshow_list.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_list(request):
    """
    Display tvshow metadata list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media_tvshow = []
    for row_data in await request.app.db_functions.db_meta_tvshow_list(db_connection, offset, per_page, request['session']['search_text']):
        media_tvshow.append((row_data['mm_metadata_tvshow_guid'],
                             row_data['mm_metadata_tvshow_name'], row_data['air_date'],
                             row_data['image_json']))
    request['session']['search_page'] = 'meta_tv'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_tvshow_list_count(db_connection,
                                request['session']['search_text']),
                            record_name='TV show(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_tvshow': media_tvshow,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


# tv show season detail - show guid then season #
@blueprint_user_metadata_tv.route("/meta_tvshow_season_detail/<guid>/<season>",
                                  methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_tvshow_season_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_tvshow_season_detail_page(request, guid, season):
    """
    Display metadata of tvshow season detail
    """
    data_metadata = await request.app.db_functions.db_meta_tvshow_detail(db_connection, guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
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
    data_episode_count = await request.app.db_functions.db_read_tvmeta_season_eps_list(db_connection,
        guid, int(season))
    common_global.es_inst.com_elastic_index('info', {'dataeps': data_episode_count})
    data_episode_keys = natsort.natsorted(data_episode_count)
    common_global.es_inst.com_elastic_index('info', {'dataepskeys': data_episode_keys})

    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
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
