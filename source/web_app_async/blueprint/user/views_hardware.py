"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g
from flask_login import login_required

blueprint = Blueprint("user_hardware", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
import database as database_base


@blueprint.route('/hardware')
@login_required
def user_hardware():
    """
    Display hardware page
    """
    return render_template("users/user_hardware.html",
                           phue=g.db_connection.db_device_count('Phue'))


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
