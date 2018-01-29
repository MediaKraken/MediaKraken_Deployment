"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, \
    redirect, url_for, abort
from flask_login import login_required
from flask_login import current_user

blueprint = Blueprint("user_3d", __name__, url_prefix='/users', static_folder="../static")
import logging  # pylint: disable=W0611
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_pagination
import database as database_base
from MediaKraken.public.forms import SearchForm

option_config_json, db_connection = common_config_ini.com_config_read()


# 3d
@blueprint.route('/3D')
@blueprint.route('/3D/')
@login_required
def user_3d_list():
    """
    Display 3D media page
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    form = SearchForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            pass
        mediadata = g.db_connection.db_meta_movie_list(offset, per_page,
                                                       request.form['search_text'])
    else:
        mediadata = g.db_connection.db_meta_movie_list(offset, per_page)

    return render_template("users/user_3d_list.html", form=form)


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
