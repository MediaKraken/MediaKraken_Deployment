"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, render_template, g, request
from flask_login import login_required

blueprint = Blueprint("user_metadata_tv", __name__, url_prefix='/users',
                      static_folder="../static")
import natsort
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_pagination
import database as database_base
from MediaKraken.public.forms import SearchForm

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_tvshow_detail/<guid>/')
@blueprint.route('/meta_tvshow_detail/<guid>')
@login_required
def metadata_tvshow_detail(guid):
    """
    Display metadata of tvshow
    """
    data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    common_global.es_inst.com_elastic_index('info', {'meta tvshow json': json_metadata})
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
                           data_season_count=sorted(
                               data_season_data.iterkeys()),
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
    data_episode_count = g.db_connection.db_read_tvmeta_season_eps_list(
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
                           data_episode_count=data_episode_count,
                           data_episode_keys=data_episode_keys
                           )


# tv show season detail - show guid then season #
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<eps_id>", methods=['GET', 'POST'])
@blueprint.route("/meta_tvshow_episode_detail/<guid>/<eps_id>/", methods=['GET', 'POST'])
@login_required
def metadata_tvshow_episode_detail_page(guid, eps_id):
    """
    Display tvshow episode metadata detail
    """
    data_metadata = g.db_connection.db_read_tvmeta_epsisode_by_id(guid, eps_id)
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
                           data_title=data_metadata['eps_name'],
                           data_runtime=data_metadata['eps_runtime'],
                           data_overview=data_metadata['eps_overview'],
                           data_first_aired=data_metadata['eps_first_air'],
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
                           )


@blueprint.route('/meta_tvshow_list', methods=['GET', 'POST'])
@blueprint.route('/meta_tvshow_list/', methods=['GET', 'POST'])
@login_required
def metadata_tvshow_list():
    """
    Display tvshow metadata list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media_tvshow = []
    form = SearchForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        mediadata = g.db_connection.db_meta_tvshow_list(offset, per_page,
                                                        request.form['search_text'])
    else:
        mediadata = g.db_connection.db_meta_tvshow_list(offset, per_page)
    for row_data in mediadata:
        media_tvshow.append((row_data['mm_metadata_tvshow_guid'],
                             row_data['mm_metadata_tvshow_name'], row_data[2],
                             row_data[3]))  # TODO dictcursor
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_tvshow_list_count(),
                                                  record_name='TV Shows',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_tvshow_list.html', form=form,
                           media_tvshow=media_tvshow,
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
def teardown_request(exception):  # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
