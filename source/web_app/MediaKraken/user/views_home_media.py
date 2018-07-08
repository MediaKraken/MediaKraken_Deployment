"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_home", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


# home media
@blueprint.route('/home_media', methods=['GET', 'POST'])
@login_required
def home_media_list():
    """
    Display mage page for home media
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    if session['search_text'] is not None:
        # TODO wrong movie query
        metadata = g.db_connection.db_meta_movie_list(offset, per_page, session['search_text'])
    else:
        metadata = g.db_connection.db_meta_movie_list(offset, per_page)
    return render_template("users/user_home_media_list.html", media=media)


@blueprint.route('/home_media_detail/<guid>')
@login_required
def home_media_detail(guid):
    """
    Display mage page for home media
    """
    pass

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
