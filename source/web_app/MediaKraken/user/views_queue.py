"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, render_template, g, request, \
    redirect, url_for, session
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_queue", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_pagination
import database as database_base
import natsort

option_config_json, db_connection = common_config_ini.com_config_read()


# list of tv shows
@blueprint.route("/queue", methods=['GET', 'POST'])
@blueprint.route("/queue/", methods=['GET', 'POST'])
@login_required
def user_queue_page():
    """
    Display queue page
    """
    page, per_page, offset = common_pagination.get_page_items()
    # list_type, list_genre = None, list_limit = 500000, group_collection = False, offset = 0
    media = []
    if session['search_text'] is not None:
        mediadata = g.db_connection.db_web_tvmedia_list(offset, per_page, session['search_text'])
    else:
        mediadata = g.db_connection.db_web_tvmedia_list(offset, per_page)
    for row_data in mediadata:
        # 0 - mm_metadata_tvshow_name, 1 - mm_metadata_tvshow_guid, 2 - count(*) mm_count,
        # 3 - mm_metadata_tvshow_localimage_json
        try:
            media.append((row_data['mm_metadata_tvshow_name'],
                          row_data['mm_metadata_tvshow_guid'],
                          row_data['mm_metadata_tvshow_localimage_json'],
                          common_internationalization.com_inter_number_format(
                              row_data['mm_count'])))
        except:
            media.append((row_data['mm_metadata_tvshow_name'],
                          row_data['mm_metadata_tvshow_guid'],
                          None, common_internationalization.com_inter_number_format(
                row_data['mm_count'])))
    session['search_page'] = 'media_tv'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_tvmedia_list_count(
                                                      None, None),
                                                  record_name='tv shows',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_tv_page.html', media=media,
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
