"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_sports", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_pagination
import database as database_base


@blueprint.route('/meta_sports_list', methods=['GET', 'POST'])
@login_required
def metadata_sports_list():
    """
    Display sports metadata list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_meta_sports_list(
            offset, per_page, session['search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    session['search_page'] = 'meta_sports'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_sports_list_count(
                                                      session['search_text']),
                                                  record_name='sporting event(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_sports_list.html',
                           media_sports_list=g.db_connection.db_meta_sports_list(offset, per_page,
                                                                                 session[
                                                                                     'search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_sports_detail/<guid>')
@login_required
def metadata_sports_detail(guid):
    """
    Display sports detail metadata
    """
    return render_template('users/metadata/meta_sports_detail.html', guid=guid,
                           data=g.db_connection.db_meta_sports_guid_by_thesportsdb(guid))


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