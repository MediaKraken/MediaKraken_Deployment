"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, \
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from fractions import Fraction

blueprint = Blueprint("user_metadata_periodical", __name__, url_prefix='/users',
                      static_folder="../static")
import logging  # pylint: disable=W0611
import subprocess
import natsort
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_internationalization
from common import common_pagination
from common import common_string
import database as database_base
from MediaKraken.public.forms import SearchForm

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_periodical_list')
@blueprint.route('/meta_periodical_list/')
@login_required
def metadata_periodical_list():
    """
    Display periodical list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    item_list = []
    form = SearchForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        mediadata = g.db_connection.db_meta_book_list(offset, per_page,
                                                      request.form['search_text'])
    else:
        mediadata = g.db_connection.db_meta_book_list(offset, per_page)
    for item_data in mediadata:
        logging.info('person data: %s', item_data)
        item_image = "/static/images/missing_icon.jpg"
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
    return render_template('users/metadata/meta_periodical_list.html', form=form,
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
    json_metadata = g.db_connection.db_meta_book_by_uuid(guid)
    try:
        data_name = json_metadata['mm_metadata_book_json']['title']
    except:
        data_name = 'NA'
    try:
        data_isbn = isbn.format(json_metadata['mm_metadata_book_json']['isbn10'])
    except:
        data_isbn = 'NA'
    try:
        data_overview = json_metadata['mm_metadata_book_json']['summary']
    except:
        data_overview = 'NA'
    try:
        data_author = json_metadata['mm_metadata_book_json']['author_data'][0]['name']
    except:
        data_author = 'NA'
    try:
        data_publisher = json_metadata['mm_metadata_book_json']['publisher_name']
    except:
        data_publisher = 'NA'
    try:
        data_pages = json_metadata['mm_metadata_book_json']['physical_description_text']
    except:
        data_pages = 'NA'
    return render_template('users/metadata/meta_periodical_detail.html',
                           data_name=data_name,
                           data_isbn=data_isbn,
                           data_overview=data_overview,
                           data_author=data_author,
                           data_publisher=data_publisher,
                           data_pages=data_pages,
                           data_item_image="/static/images/missing_icon.jpg",
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
