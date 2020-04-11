"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint("user_game_dedicated_server", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_pagination_flask
import database as database_base


@blueprint.route('/game_servers', methods=['GET', 'POST'])
@login_required
def user_game_server_list():
    """
    Display game server page
    """
    page, per_page, offset = common_pagination_flask.get_page_items()
    pagination = common_pagination_flask.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.
                                                  db_game_server_list_count(),
                                                  record_name='game servers(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("users/user_game_dedicated_servers.html",
                           media=g.db_connection.db_game_server_list(offset, per_page),
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
