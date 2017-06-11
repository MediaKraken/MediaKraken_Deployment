"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
blueprint = Blueprint("user_tv", __name__, url_prefix='/users', static_folder="../static")
#import locale
#locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_internationalization
from common import common_pagination
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


# list of tv shows
@blueprint.route("/tv")
@blueprint.route("/tv/")
@login_required
def user_tv_page():
    """
    Display tv shows page
    """
    page, per_page, offset = common_pagination.get_page_items()
    # list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
    media = []
    for row_data in g.db_connection.db_web_tvmedia_list(None, per_page, False, offset):
        # 0 - mm_metadata_tvshow_name, 1 - mm_metadata_tvshow_guid, 2 - count(*) mm_count,
        # 3 - mm_metadata_tvshow_localimage_json
        try:
            media.append((row_data['mm_metadata_tvshow_name'], row_data['mm_metadata_tvshow_guid'],
                row_data['mm_metadata_tvshow_localimage_json'],
                common_internationalization.com_inter_number_format(row_data['mm_count'])))
        except:
            media.append((row_data['mm_metadata_tvshow_name'], row_data['mm_metadata_tvshow_guid'],
                None, common_internationalization.com_inter_number_format(row_data['mm_count'])))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_tvmedia_list_count(
                                                      None, None),
                                                  record_name='media',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_tv_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


# tv show detail
@blueprint.route("/tv_show_detail/<guid>", methods=['GET', 'POST'])
@blueprint.route("/tv_show_detail/<guid>/", methods=['GET', 'POST'])
@login_required
def user_tv_show_detail_page(guid):
    """
    Display tv show detail page
    """
    if request.method == 'POST':
        # do NOT need to check for play video here,
        # it's routed by the event itself in the html via the 'action' clause
        if request.form['status'] == 'Watched':
            g.db_connection.db_media_watched_status_update(guid, current_user.get_id(), False)
            return redirect(url_for('user.user_tv_show_detail_page', guid=guid))
        elif request.form['status'] == 'Unwatched':
            g.db_connection.db_media_watched_status_update(guid, current_user.get_id(), True)
            return redirect(url_for('user.user_tv_show_detail_page', guid=guid))
    else:
        # guid, name, id, metajson
        data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
        json_metadata = data_metadata['mm_metadata_tvshow_json']
        if 'tvmaze' in json_metadata['Meta']:
            #data_runtime = json_metadata.get(['Meta']['tvmaze']['runtime'], None)
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
                    '').replace('</p>', '')
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
        data_vote_count = 0 # common_internationlzia.('%d', json_metadata['vote_count'], True)

        # build production list
        production_list = ''
        #for ndx in range(0,len(json_metadata['production_companies'])):
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
        #review = g.db_connection.db_Review_List(data[0])
        data_season_data = g.db_connection.db_read_tvmeta_eps_season(guid)
        data_season_count = sorted(data_season_data.iterkeys())
        # calculate a better runtime
        minutes, seconds = divmod((float(data_runtime) * 60), 60)
        hours, minutes = divmod(minutes, 60)
        # set watched
        try:
            watched_status = json_metadata['UserStats'][current_user.get_id()]
        except:
            watched_status = False
        return render_template('users/user_tv_show_detail.html', data=data_metadata[0],
                               json_metadata=json_metadata,
                               data_genres=data_genres_list[:-2],
                               data_production=production_list[:-2],
                               data_guid=guid,
                               data_overview=data_overview,
                               data_rating=data_rating,
                               data_first_aired=data_first_aired,
                               # data_review=review,
                               data_poster_image=data_poster_image,
                               data_background_image=data_background_image,
                               data_vote_count=data_vote_count,
                               data_watched_status=watched_status,
                               data_season_data=data_season_data,
                               data_season_count=data_season_count,
                               data_runtime="%02dH:%02dM:%02dS" % (hours, minutes, seconds)
                              )


# tv show season detail - show guid then season #
@blueprint.route("/tv_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@blueprint.route("/tv_season_detail/<guid>/<season>/", methods=['GET', 'POST'])
@login_required
def user_tv_season_detail_page(guid, season):
    """
    Display tv season detail page
    """
    data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
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
            data_overview\
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

    data_episode_count = g.db_connection.db_read_tvmeta_season_eps_list(guid, int(season))
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
    return render_template("users/user_tv_season_detail.html", data=data_metadata[0],
                           data_guid=guid,
                           data_season=season,
                           data_overview=data_overview,
                           data_rating=data_rating,
                           data_first_aired=data_first_aired,
                           data_runtime=data_runtime,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           data_episode_count=data_episode_count
                          )


# tv show episode detail
@blueprint.route("/tv_episode_detail/<guid>/<season>/<episode>", methods=['GET', 'POST'])
@blueprint.route("/tv_episode_detail/<guid>/<season>/<episode>/", methods=['GET', 'POST'])
@login_required
def user_tv_episode_detail_page(guid, season, episode):
    """
    Display tv episode detail page
    """
    data_episode_detail = g.db_connection.db_read_tvmeta_episode(guid, season, episode)
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
    return render_template("users/user_tv_episode_detail.html", data=data_episode_detail,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
                          )


@blueprint.route('/meta_tvshow_detail/<guid>/')
@blueprint.route('/meta_tvshow_detail/<guid>')
@login_required
def metadata_tvshow_detail(guid):
    """
    Display metadata of tvshow
    """
    data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    logging.info('meta tvshow json: %s', json_metadata)
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
            data_overview\
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
        if 'Genre' in json_metadata['Meta']['thetvdb']['Meta']['Series']\
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
    data_season_data = g.db_connection.db_read_tvmeta_eps_season(guid)
#    # build production list
#    production_list = ''
#    for ndx in range(0,len(json_metadata['production_companies'])):
#        production_list += (json_metadata['production_companies'][ndx]['name'] + ', ')
    return render_template('users/metadata/meta_tvshow_detail.html',
                           data_title=data_metadata['mm_metadata_tvshow_name'],
                           data_runtime=data_runtime,
                           data_guid=guid,
                           data_rating=data_rating,
                           data_first_aired=data_first_aired,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           data_overview=data_overview,
                           data_season_data=data_season_data,
                           data_season_count=sorted(data_season_data.iterkeys()),
                           data_genres_list=data_genres_list[:-2]
                          )


# tv show season detail - show guid then season #
@blueprint.route("/meta_tvshow_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@blueprint.route("/meta_tvshow_season_detail/<guid>/<season>/", methods=['GET', 'POST'])
@login_required
def metadata_tvshow_season_detail_page(guid, season):
    """
    Display metadata of tvshow season detail
    """
    data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
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
            data_overview\
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
    data_episode_count = g.db_connection.db_read_tvmeta_season_eps_list(guid, int(season))
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
    return render_template("users/metadata/meta_tvshow_season_detail.html",
                           data=data_metadata['mm_metadata_tvshow_name'],
                           data_guid=guid,
                           data_season=season,
                           data_overview=data_overview,
                           data_rating=data_rating,
                           data_first_aired=data_first_aired,
                           data_runtime=data_runtime,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           data_episode_count=data_episode_count
                          )


# tv show season detail - show guid then season #
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<eps_id>", methods=['GET', 'POST'])
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<eps_id>/", methods=['GET', 'POST'])
@login_required
def metadata_tvshow_episode_detail_page(guid, episode_id):
    """
    Display tvshow episode metadata detail
    """
    data_metadata = g.db_connection.db_read_tvmeta_epsisode_by_id(guid, episode_id)
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
    return render_template("users/metadata/meta_tvshow_episode_detail.html", data=data_metadata[0],
                           data_guid=guid,
                           data_title=data_metadata[2],
                           data_runtime=data_metadata[4],
                           data_season=season,
                           data_episode=episode,
                           data_overview=data_metadata[5],
                           data_first_aired=data_metadata[3],
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
                          )


@blueprint.route('/meta_tvshow_list')
@blueprint.route('/meta_tvshow_list/')
@login_required
def metadata_tvshow_list():
    """
    Display tvshow metadata list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media_tvshow = []
    for row_data in g.db_connection.db_meta_tvshow_list(offset, per_page):
        media_tvshow.append((row_data['mm_metadata_tvshow_guid'],
            row_data['mm_metadata_tvshow_name'], row_data[2], row_data[3])) # TODO dictcursor
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_tvshow_list_count(),
                                                  record_name='TV Shows',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_tvshow_list.html', media_tvshow=media_tvshow,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception): # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
