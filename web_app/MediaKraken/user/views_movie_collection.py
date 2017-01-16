"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify,\
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user
from fractions import Fraction
blueprint = Blueprint("user_movie_collection", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_google
from common import common_pagination
from common import common_string
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_movie_collection_list')
@blueprint.route('/meta_movie_collection_list/')
@login_required
def metadata_movie_collection_list():
    """
    Display movie collection metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_collection_list(offset, per_page):
        try:
            media.append((row_data['mm_metadata_collection_guid'],\
                row_data['mm_metadata_collection_name'],\
                row_data['mm_metadata_collection_imagelocal_json']['Poster']))
        except:
            media.append((row_data['mm_metadata_collection_guid'],\
                row_data['mm_metadata_collection_name'], None))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(\
                                                      'mm_metadata_collection'),
                                                  record_name='movie collection(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template('users/metadata/meta_movie_collection_list.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/meta_movie_collection_detail/<guid>/')
@blueprint.route('/meta_movie_collection_detail/<guid>')
@login_required
def metadata_movie_collection_detail(guid):
    """
    Display movie collection metadata detail
    """
    data_metadata = g.db_connection.db_collection_read_by_guid(guid)
    json_metadata = data_metadata['mm_metadata_collection_json']
    json_imagedata = data_metadata['mm_metadata_collection_imagelocal_json']
    # poster image
    try:
        if json_imagedata['Poster'] is not None:
            data_poster_image = json_imagedata['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_imagedata['Backdrop'] is not None:
            data_background_image = json_imagedata['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template('users/metadata/meta_movie_collection_detail.html',
                           data_name=json_metadata['name'],
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           json_metadata=json_metadata
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
