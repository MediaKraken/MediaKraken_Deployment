# -*- coding: utf-8 -*-

import json
import sys

sys.path.append('..')
from quart import Blueprint, render_template, g, request, flash
from flask_login import login_required

blueprint = Blueprint("admins_link", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import quart
from flask_login import current_user
from functools import wraps
from MediaKraken.admins.forms import LinkAddEditForm

from common import common_config_ini
from common import common_global
from common import common_pagination
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
            return quart.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/link_server")
@login_required
@admin_required
async def admin_server_link_server():
    """
    Display page for linking server
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_link_list_count(),
                                                  record_name='linked servers',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template("admin/admin_link.html",
                           data=g.db_connection.db_link_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@blueprint.route("/link_edit", methods=["GET", "POST"])
@login_required
@admin_required
async def admin_link_edit_page():
    """
    allow user to edit link
    """
    form = LinkAddEditForm(await request.form)
    return await render_template("admin/admin_link_edit.html", form=form,
                           data_class=None,
                           data_share=None)


@blueprint.route('/link_delete', methods=["POST"])
@login_required
@admin_required
async def admin_link_delete_page():
    """
    Delete linked server action 'page'
    """
    g.db_connection.db_link_delete(await request.form['id'])
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
