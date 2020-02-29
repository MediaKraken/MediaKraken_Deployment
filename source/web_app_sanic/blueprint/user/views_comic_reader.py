"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint("user_comic_view", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
import database as database_base


@blueprint.route('/comic_view/<guid>')
@login_required
def user_comic_view(guid):
    """
    Display image comic view
    """
    return render_template("users/user_comic_view.html",
                           comic_data=g.db_connection.db_media_path_by_uuid(guid))


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