"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, redirect, url_for, flash
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")
import json
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display each error on top of form
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@blueprint.route("/")
@login_required
def members():
    """
    Display main members page
    """
    return render_template("users/members.html",
                           data_new_media=g.db_connection.db_read_media_new_count(7))


@blueprint.route('/movie_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
def movie_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie status': guid, 'event': event_type})
    if event_type == "sync":
        return redirect(url_for('user.sync_edit', guid=guid))
    else:
        if event_type == "mismatch":
            # TODO ummmm, how do I know which specific media to update?
            # TODO as some might be right
            g.db_connection.db_media_status_update(
                g.db_connection.db_metadata_from_media_guid(guid),
                current_user.get_id(), event_type)
            return json.dumps({'status': 'OK'})
        else:
            # g.db_connection.db_media_rating_update(
            #     guid, current_user.get_id(), event_type)
            g.db_connection.db_meta_movie_status_update(
                g.db_connection.db_metadata_from_media_guid(guid),
                current_user.get_id(), event_type)
            return json.dumps({'status': 'OK'})


@blueprint.route('/movie_metadata_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
def movie_metadata_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie metadata status': guid,
                                                     'event': event_type})
    g.db_connection.db_meta_movie_status_update(
        guid, current_user.get_id(), event_type)
    return json.dumps({'status': 'OK'})


@blueprint.route('/tv_status/<guid>/<event_type>', methods=['GET', 'POST'])
@login_required
def tv_status(guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'tv status': guid, 'event': event_type})
    if event_type == "watched":
        pass
    elif event_type == "sync":
        pass
    elif event_type == "favorite":
        pass
    elif event_type == "poo":
        pass
    elif event_type == "mismatch":
        pass
    return redirect(url_for('user_tv.user_tv_page'))


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
