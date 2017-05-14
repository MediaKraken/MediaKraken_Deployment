# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
#import locale
#locale.setlocale(locale.LC_ALL, '')
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
blueprint = Blueprint("admins", __name__, url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from functools import partial
from MediaKraken.admins.forms import AdminSettingsForm

from common import common_config_ini
from common import common_internationalization
from common import common_version
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


@blueprint.route("/tvtuners", methods=["GET", "POST"])
@blueprint.route("/tvtuners/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_tvtuners():
    """
    List tvtuners
    """
    tv_tuners = []
    for row_data in g.db_connection.db_tuner_list():
        tv_tuners.append((row_data['mm_tuner_id'], row_data['mm_tuner_json']['HWModel']\
        + " (" + row_data['mm_tuner_json']['Model'] + ")", row_data['mm_tuner_json']['IP'],
        row_data['mm_tuner_json']['Active'], len(row_data['mm_tuner_json']['Channels'])))
    return render_template("admin/admin_tvtuners.html", data_tuners=tv_tuners)


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
