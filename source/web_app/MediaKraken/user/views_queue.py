"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_queue", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route("/queue", methods=['GET', 'POST'])
@login_required
def user_queue_page():
    """
    Display queue page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    mediadata = g.db_connection.db_meta_queue_list(current_user.get_id(), offset, per_page,
                                                   session['search_text'])
    # TODO union read all four.....then if first "group"....add header in the html
    session['search_page'] = 'user_media_queue'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_tvmedia_list_count(
                                                      None, None, session['search_text']),
                                                  record_name='queue',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_queue.html', media=media,
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
