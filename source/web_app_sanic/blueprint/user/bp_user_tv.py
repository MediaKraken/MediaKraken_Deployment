import natsort
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch_httpx
from common import common_pagination_bootstrap
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_tv = Blueprint('name_blueprint_user_tv', url_prefix='/user')


@blueprint_user_tv.route("/user_tv", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_tv.html')
@common_global.auth.login_required
async def url_bp_user_tv(request):
    """
    Display tv shows page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    # list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
    media = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_media_tv_list(db_connection, offset,
                                                                    int(request.ctx.session[
                                                                            'per_page']),
                                                                    request.ctx.session[
                                                                        'search_text']):
        # 0 - mm_metadata_tvshow_name, 1 - mm_metadata_tvshow_guid, 2 - count(*) mm_count,
        # 3 - mm_metadata_tvshow_localimage_json
        try:
            media.append((row_data['mm_metadata_tvshow_name'],
                          row_data['mm_metadata_tvshow_guid'],
                          row_data['mm_metadata_tvshow_localimage_json'],
                          common_internationalization.com_inter_number_format(
                              row_data['mm_count'])))
        except:
            media.append((row_data['mm_metadata_tvshow_name'],
                          row_data['mm_metadata_tvshow_guid'],
                          None, common_internationalization.com_inter_number_format(
                row_data['mm_count'])))
    request.ctx.session['search_page'] = 'media_tv'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_tv',
                                                                      item_count=await request.app.db_functions.db_media_tv_list_count(
                                                                          db_connection,
                                                                          None, None,
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


@blueprint_user_tv.route("/user_tv_show_detail/<guid>", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_tv_show_detail.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_tv_show_detail(request, user, guid):
    """
    Display tv show detail page
    """
    db_connection = await request.app.db_pool.acquire()
    if request.method == 'POST':
        # do NOT need to check for play video here,
        # it's routed by the event itself in the html via the 'action' clause
        if request.form['status'] == 'Watched':
            await request.app.db_functions.db_meta_tv_status_update(db_connection,
                                                                    guid, user.id, False)
            return redirect(
                request.app.url_for('name_blueprint_user_tv.url_bp_user_tv_show_detail', guid=guid))
        elif request.form['status'] == 'Unwatched':
            await request.app.db_functions.db_meta_tv_status_update(db_connection,
                                                                    guid, user.id, True)
            return redirect(
                request.app.url_for('name_blueprint_user_tv.url_bp_user_tv_show_detail', guid=guid))
    else:
        # guid, name, id, metajson
        data_metadata = await request.app.db_functions.db_meta_tv_detail(db_connection, guid)
        json_metadata = data_metadata['mm_metadata_tvshow_json']
        if 'tvmaze' in json_metadata['Meta']:
            # data_runtime = json_metadata.get(['Meta']['tvmaze']['runtime'], None)
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
                data_overview = json_metadata['Meta']['tvmaze']['summary'].replace('<p>',
                                                                                   '').replace(
                    '</p>', '')
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
            if 'Genre' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
                for ndx in json_metadata['Meta']['thetvdb']['Meta']['Series']['Genre'].split("|"):
                    data_genres_list += (ndx + ', ')
                # since | is at first and end....chop off first and last comma
                data_genres_list = data_genres_list[2:-2]

        # vote count format
        # common_internationlzia.('%d', json_metadata['vote_count'], True)
        data_vote_count = 0

        # build production list
        production_list = ''
        # for ndx in range(0,len(json_metadata['production_companies'])):
        #    production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
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
        # grab reviews
        review = await request.app.db_functions.db_review_list_by_tmdb_guid(db_connection, guid)
        data_season_data = await request.app.db_functions.db_meta_tv_eps_season(db_connection, guid)
        data_season_count = sorted(data_season_data.iterkeys())
        # calculate a better runtime
        minutes, seconds = divmod((float(data_runtime) * 60), 60)
        hours, minutes = divmod(minutes, 60)
        # set watched
        try:
            watched_status = json_metadata['UserStats'][user.id]
        except:
            watched_status = False
        await request.app.db_pool.release(db_connection)
        return {

            'data': data_metadata[0],
            'json_metadata': json_metadata,
            'data_genres': data_genres_list[:-2],
            'data_production': production_list[:-2],
            'data_guid': guid,
            'data_overview': data_overview,
            'data_rating': data_rating,
            'data_first_aired': data_first_aired,
            # data_review=review,
            'data_poster_image': data_poster_image,
            'data_background_image': data_background_image,
            'data_vote_count': data_vote_count,
            'data_watched_status': watched_status,
            'data_season_data': data_season_data,
            'data_season_count': data_season_count,
            'data_runtime': "%02dH:%02dM:%02dS" % (
                hours, minutes, seconds)
        }
    await request.app.db_pool.release(db_connection)


@blueprint_user_tv.route("/user_tv_show_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_tv_show_season_detail.html')
@common_global.auth.login_required
async def url_bp_user_tv_show_season_detail_page(request, guid, season):
    """
    Display tv season detail page
    """
    db_connection = await request.app.db_pool.acquire()
    data_metadata = await request.app.db_functions.db_meta_tv_detail(db_connection, guid)
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
        if 'Genre' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            for ndx in json_metadata['Meta']['thetvdb']['Meta']['Series']['Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]
    data_episode_count = await request.app.db_functions.db_meta_tv_season_eps_list(db_connection,
                                                                                   guid,
                                                                                   int(season))
    await request.app.db_pool.release(db_connection)
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        'dataeps': data_episode_count})
    data_episode_keys = natsort.natsorted(data_episode_count)
    common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        'dataepskeys': data_episode_keys})
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
        'data': data_metadata[0],
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


@blueprint_user_tv.route("/user_tv_show_episode_detail/<guid>/<season>/<episode>",
                         methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/media/bss_user_media_tv_show_episode_detail.html')
@common_global.auth.login_required
async def url_bp_user_tv_show_episode_detail_page(request, guid, season, episode):
    """
    Display tv episode detail page
    """
    db_connection = await request.app.db_pool.acquire()
    data_episode_detail = await request.app.db_functions.db_meta_tv_episode(db_connection,
                                                                            guid, season, episode)
    await request.app.db_pool.release(db_connection)
    # poster image
    try:
        data_poster_image = data_episode_detail[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_episode_detail['LocalImages']['Backdrop'] is not None:
            data_background_image = data_episode_detail['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return {
        'data': data_episode_detail,
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
    }
