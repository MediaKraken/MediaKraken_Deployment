# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
from flask import Blueprint, render_template, g, flash, request
from flask_login import login_required

blueprint = Blueprint("admins_game", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps

from common import common_config_ini
from common import common_docker
from common import common_global
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
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/game_metadata", methods=["GET", "POST"])
@login_required
@admin_required
def game_metadata():
    """
    Game metadata stats and update screen
    """
    if request.method == 'POST':
        docker_inst = common_docker.CommonDocker()
        docker_inst.com_docker_run_game_data()
    data_mame_version = None
    return render_template("admin/admin_games_metadata.html",
                           data_mame_version=data_mame_version,
                           )


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
