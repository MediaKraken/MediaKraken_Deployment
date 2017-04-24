"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from MediaKraken.user.forms import BookAddForm
blueprint = Blueprint("user_periodicals", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import json
import sys
import uuid
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


# books
@blueprint.route('/books')
@blueprint.route('/books/')
@login_required
def user_books_list():
    """
    Display books page
    """
    return render_template("users/user_books_list.html")


@blueprint.route('/meta_periodical_list')
@blueprint.route('/meta_periodical_list/')
@login_required
def metadata_periodical_list():
    """
    Display periodical list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    item_list = []
    for item_data in g.db_connection.db_meta_book_list(offset, per_page):
        logging.info('person data: %s', item_data)
        item_image = "../../static/images/Missing_Icon.png"
        item_list.append((item_data['mm_metadata_book_guid'],
                          item_data['mm_metadata_book_name'], item_image))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_book'),
                                                  record_name='Periodical',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_periodical_list.html',
                           media_person=item_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_periodical_detail/<guid>/')
@blueprint.route('/meta_periodical_detail/<guid>')
@login_required
def metadata_periodical_detail(guid):
    """
    Display periodical detail page
    """
    return render_template('users/metadata/meta_periodical_detail.html',
                           json_metadata=g.db_connection.db_meta_book_by_uuid(guid),
                           data_item_image="../../static/images/Missing_Icon.png",
                          )


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception): # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
