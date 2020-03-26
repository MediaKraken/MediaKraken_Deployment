"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_newmedia", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_pagination_flask
import database as database_base


@blueprint.route('/new_media', methods=['GET', 'POST'])
@login_required
def user_newmedia_page():
    """
    Display new media
    """
    page, per_page, offset = common_pagination_flask.get_page_items()
    session['search_page'] = 'new_media'
    media_data = []
    for media_file in g.db_connection.db_read_media_new(offset, per_page, session['search_text'],
                                                        days_old=7):
        media_data.append(
            (media_file['mm_media_class_guid'],
             media_file['mm_media_name'], None))
    pagination = common_pagination_flask.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_read_media_new_count(
                                                      session['search_text'],
                                                      days_old=7),
                                                  record_name='new media',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_newmedia.html',
                           media=media_data,
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
