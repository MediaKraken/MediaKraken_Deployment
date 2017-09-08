# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import uuid
import pygal
import json
import logging # pylint: disable=W0611
import os
import sys
sys.path.append('..')
from flask import Blueprint, render_template, g, request, current_app, jsonify, flash,\
     url_for, redirect, session, abort
from flask_login import login_required
from flask_paginate import Pagination
blueprint = Blueprint("admins_messages", __name__, url_prefix='/admin',
                      static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from functools import partial

from common import common_config_ini
from common import common_internationalization
from common import common_network_cifs
from common import common_pagination
from common import common_string
import database as database_base


option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display errors from list
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def admin_required(fn):
    """
    Admin check
    """
    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        logging.info("admin access attempt by %s" % current_user.get_id())
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)
    return decorated_view


@blueprint.route("/messages", methods=["GET", "POST"])
@blueprint.route("/messages/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_messages():
    """
    List all messages
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_messages'),
                                                  record_name='messages(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("admin/admin_messages.html",
                           media_dir=g.db_connection.db_message_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/message_delete', methods=["POST"])
@login_required
@admin_required
def admin_messages_delete_page():
    """
    Delete messages action 'page'
    """
    g.db_connection.db_message_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    g.db_connection.db_close()
