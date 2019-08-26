"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
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
@login_required
def user_books_list():
    """
    Display books page
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'media_periodicals'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_book_list_count(
                                                      session['search_text']),
                                                  record_name='periodical(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    media_list = g.db_connection.db_media_book_list(offset, per_page, session['search_text'])
    session['search_text'] = None
    return render_template("users/user_books_list.html",
                           media=media_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/book_detail/<guid>')
@login_required
def user_books_detail(guid):
    """
    Display books page
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
