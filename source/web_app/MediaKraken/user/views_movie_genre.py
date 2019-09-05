"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_movie_genre", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route("/movie_genre", methods=['GET', 'POST'])
@login_required
def user_movie_genre_page():
    """
    Display movies split up by genre
    """
    media = []
    for row_data in g.db_connection.db_media_movie_count_by_genre(
            common_global.DLMediaType.Movie):
        media.append((row_data['gen']['name'],
                      common_internationalization.com_inter_number_format(
                          row_data[1]),
                      row_data[0]['name'] + ".png"))
    return render_template('users/user_movie_genre_page.html', media=sorted(media))


@blueprint.route("/movie/<genre>", methods=['GET', 'POST'])
@login_required
def user_movie_page(genre):
    """
    Display movie page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_web_media_list(
            common_global.DLMediaType.Movie,
            list_type='movie', list_genre=genre, list_limit=per_page, group_collection=False,
            offset=offset, include_remote=True, search_text=session['search_text']):
        # 0- mm_media_name, 1- mm_media_guid, 2- mm_metadata_user_json,
        # 3 - mm_metadata_localimage_json
        common_global.es_inst.com_elastic_index('info',
                                                {"row2": row_data['mm_metadata_user_json']})
        json_image = row_data['mm_metadata_localimage_json']
        # set watched
        try:
            watched_status \
                = row_data['mm_metadata_user_json']['UserStats'][current_user.get_id()]['watched']
        except (KeyError, TypeError):
            watched_status = False
        # set synced
        try:
            sync_status = \
                row_data['mm_metadata_user_json']['UserStats'][current_user.get_id()]['sync']
        except (KeyError, TypeError):
            sync_status = False
        # set rating
        if row_data['mm_metadata_user_json'] is not None \
                and 'UserStats' in row_data['mm_metadata_user_json'] \
                and current_user.get_id() in row_data['mm_metadata_user_json']['UserStats'] \
                and 'Rating' in row_data['mm_metadata_user_json']['UserStats'][
            current_user.get_id()]:
            rating_status \
                = row_data['mm_metadata_user_json']['UserStats'][current_user.get_id()]['Rating']
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
    total = g.db_connection.db_web_media_list_count(
        common_global.DLMediaType.Movie, list_type='movie', list_genre=genre,
        group_collection=False, include_remote=True, search_text=session['search_text'])
    session['search_page'] = 'media_movie'
    session['search_text'] = None
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=total,
                                                  record_name='movie(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_movie_page.html', media=media,
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
