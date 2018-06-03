"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, render_template, g, request, session
from flask_login import login_required

blueprint = Blueprint("user_periodicals", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


# books
@blueprint.route('/books', methods=['GET', 'POST'])
@blueprint.route('/books/', methods=['GET', 'POST'])
@blueprint.route('/books/<search_text>/', methods=['GET', 'POST'])
@login_required
def user_books_list():
    """
    Display books page
    """
    page, per_page, offset = common_pagination.get_page_items()
    if request.method == 'POST':
        mediadata = g.db_connection.db_media_book_list(offset, per_page, search_text)
    else:
        mediadata = g.db_connection.db_media_book_list(offset, per_page)
    return render_template("users/user_books_list.html", media=mediadata)


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
