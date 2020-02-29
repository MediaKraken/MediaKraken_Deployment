"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_periodical", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_global
from common import common_isbn
from common import common_pagination
import database as database_base


@blueprint.route('/meta_periodical_list', methods=['GET', 'POST'])
@login_required
def metadata_periodical_list():
    """
    Display periodical list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    item_list = []
    for item_data in g.db_connection.db_meta_book_list(offset, per_page, session['search_text']):
        common_global.es_inst.com_elastic_index('info', {'person data': item_data})
        item_image = "/static/images/missing_icon.jpg"
        item_list.append((item_data['mm_metadata_book_guid'],
                          item_data['mm_metadata_book_name'], item_image))
    session['search_page'] = 'meta_periodical'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_book_list_count(
                                                      session['search_text']),
                                                  record_name='periodical(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_periodical_list.html',
                           media_person=item_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_periodical_detail/<guid>')
@login_required
def metadata_periodical_detail(guid):
    """
    Display periodical detail page
    """
    json_metadata = g.db_connection.db_meta_book_by_uuid(guid)
    try:
        data_name = json_metadata['mm_metadata_book_json']['title']
    except KeyError:
        data_name = 'NA'
    try:
        data_isbn = common_isbn.com_isbn_mask(json_metadata['mm_metadata_book_json']['isbn10'])
    except KeyError:
        data_isbn = 'NA'
    try:
        data_overview = json_metadata['mm_metadata_book_json']['summary']
    except KeyError:
        data_overview = 'NA'
    try:
        data_author = json_metadata['mm_metadata_book_json']['author_data'][0]['name']
    except KeyError:
        data_author = 'NA'
    try:
        data_publisher = json_metadata['mm_metadata_book_json']['publisher_name']
    except KeyError:
        data_publisher = 'NA'
    try:
        data_pages = json_metadata['mm_metadata_book_json']['physical_description_text']
    except KeyError:
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