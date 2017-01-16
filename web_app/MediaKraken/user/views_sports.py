"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from flask_paginate import Pagination
from fractions import Fraction
blueprint = Blueprint("user_sports", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import json
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_google
from common import common_network_twitch
from common import common_network_vimeo
from common import common_network_youtube
from common import common_pagination
from common import common_string
import database as database_base


# list of spoting events
@blueprint.route("/sports")
@blueprint.route("/sports/")
@login_required
def user_sports_page():
    """
    Display sporting events page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_meta_sports_list(offset, per_page):
        media.append((row_data['mm_metadata_sports_guid'], row_data['mm_metadata_sports_name']))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_sports_list_count(),
                                                  record_name='sporting events',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/user_sports_page.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route("/sports_detail/<guid>/", methods=['GET', 'POST'])
@blueprint.route("/sports_detail/<guid>", methods=['GET', 'POST'])
@login_required
def user_sports_detail_page(guid):
    """
    Display sports detail page
    """
    # poster image
    try:
        if json_metadata['LocalImages']['Poster'] is not None:
            data_poster_image = json_metadata['LocalImages']['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_sports_detail.html",
                           data=g.db_connection.db_metathesportsdb_select_guid(guid),
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
                          )


@blueprint.route('/meta_sports_list')
@blueprint.route('/meta_sports_list/')
@login_required
def metadata_sports_list():
    """
    Display sports metadata list
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_sports_list_count(),
                                                  record_name='sporting events',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_sports_list.html',
                           media_sports_list=g.db_connection.db_meta_sports_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_sports_detail/<guid>/')
@blueprint.route('/meta_sports_detail/<guid>')
@login_required
def metadata_sports_detail(guid):
    """
    Display sports detail metadata
    """
    return render_template('users/metadata/meta_sports_detail.html', guid=guid,
                           data=g.db_connection.db_meta_sports_by_guid(guid))
