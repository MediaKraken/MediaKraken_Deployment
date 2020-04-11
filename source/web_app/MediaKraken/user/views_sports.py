"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_sports", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_global
from common import common_pagination_flask
import database as database_base


# list of spoting events
@blueprint.route("/sports", methods=['GET', 'POST'])
@login_required
def user_sports_page():
    """
    Display sporting events page
    """
    page, per_page, offset = common_pagination_flask.get_page_items()
    media = []
    for row_data in g.db_connection.db_media_sports_list(
            common_global.DLMediaType.Sports.value,
            offset, per_page, session['search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    session['search_page'] = 'media_sports'
    pagination = common_pagination_flask.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_sports_list_count(
                                                      session['search_text']),
                                                  record_name='sporting event(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_sports_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/sports_detail/<guid>", methods=['GET', 'POST'])
@login_required
def user_sports_detail_page(guid):
    """
    Display sports detail page
    """
    # poster image
    try:
        if json_metadata['LocalImages']['Poster'] is not None:
            data_poster_image = json_metadata['LocalImages']['Poster']
        else:
            data_poster_image = None
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
    return render_template("users/user_sports_detail.html",
                           data=g.db_connection.db_metathesportsdb_select_guid(
                               guid),
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
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
