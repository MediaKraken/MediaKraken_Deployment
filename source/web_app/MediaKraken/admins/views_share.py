# -*- coding: utf-8 -*-

import json
import os
import sys

sys.path.append('..')
from flask import Blueprint, render_template, g, request, flash, \
    url_for, redirect
from flask_login import login_required

blueprint = Blueprint("admins_share", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import flask
from flask_login import current_user
from functools import wraps
from MediaKraken.admins.forms import ShareAddEditForm

from common import common_config_ini
from common import common_global
from common import common_network_cifs
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
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/share", methods=["GET", "POST"])
@blueprint.route("/share/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_share():
    """
    List all share/mounts
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_media_share'),
                                                  record_name='share(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("admin/admin_share.html",
                           media_dir=g.db_connection.db_audit_shares(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/share_edit", methods=["GET", "POST"])
@blueprint.route("/share_edit/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_share_edit_page():
    """
    allow user to edit share
    """
    form = ShareAddEditForm(request.form)
    common_global.es_inst.com_elastic_index('info', {'stuff': 'hereeditshare'})
    if request.method == 'POST':
        common_global.es_inst.com_elastic_index('info', {'stuff': 'herepost'})
        if form.validate_on_submit():
            common_global.es_inst.com_elastic_index('info', {'action': request.form[
                'action_type']})
            if request.form['action_type'] == 'Add':
                common_global.es_inst.com_elastic_index('info', {'type': request.form[
                    'storage_mount_type']})
                # check for UNC
                if request.form['storage_mount_type'] == "unc":
                    #                    addr, share, path = common_string.com_string_unc_to_addr_path(\
                    #                        request.form['storage_mount_path'])
                    #                    if addr is None: # total junk path for UNC
                    #                        flash("Invalid UNC path.", 'error')
                    #                        return redirect(url_for('admins_share.admin_share_edit_page'))
                    #                    common_global.es_inst.com_elastic_index('info', {'stuff':'unc info: %s %s %s' % (addr, share, path))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(request.form['storage_mount_server'],
                                               user_name=request.form['storage_mount_user'],
                                               user_password=request.form['storage_mount_password'])
                    #                    if not smb_stuff.com_cifs_share_directory_check(\
                    #                            request.form['storage_mount_server'], \
                    #                            request.form['storage_mount_path']):
                    #                        smb_stuff.com_cifs_close()
                    #                        flash("Invalid UNC path.", 'error')
                    #                        return redirect(url_for('admins_share.admin_share_edit_page'))
                    smb_stuff.com_cifs_close()
                # smb/cifs mounts
                elif request.form['storage_mount_type'] == "smb":
                    # TODO
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(request.form['storage_mount_server'],
                                               user_name=request.form['storage_mount_user'],
                                               user_password=request.form['storage_mount_password'])
                    smb_stuff.com_cifs_share_directory_check(share_name,
                                                             request.form['storage_mount_path'])
                    smb_stuff.com_cifs_close()
                # nfs mount
                elif request.form['storage_mount_type'] == "nfs":
                    # TODO
                    pass
                elif not os.path.isdir(request.form['storage_mount_path']):
                    flash("Invalid share path.", 'error')
                    return redirect(url_for('admins_share.admin_share_edit_page'))
                # verify it doesn't exit and add
                if g.db_connection.db_audit_share_check(request.form['storage_mount_path']) == 0:
                    g.db_connection.db_audit_share_add(request.form['storage_mount_type'],
                                                       request.form['storage_mount_user'],
                                                       request.form['storage_mount_password'],
                                                       request.form['storage_mount_server'],
                                                       request.form['storage_mount_path'])
                    g.db_connection.db_commit()
                    return redirect(url_for('admins_share.admin_share'))
                else:
                    flash("Share already mapped.", 'error')
                    return redirect(url_for('admins_share.admin_share_edit_page'))
            elif request.form['action_type'] == 'Browse':
                # browse for smb shares on the host network
                pass
        else:
            flash_errors(form)
    return render_template("admin/admin_share_edit.html", form=form)


@blueprint.route('/share_delete', methods=["POST"])
@login_required
@admin_required
def admin_share_delete_page():
    """
    Delete share action 'page'
    """
    g.db_connection.db_audit_share_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getShareById', methods=['POST'])
@login_required
@admin_required
def getShareById():
    result = g.db_connection.db_audit_share_by_uuid(request.form['id'])
    return json.dumps({'Id': result['mm_share_dir_guid'],
                       'Path': result['mm_share_dir_path']})


@blueprint.route('/updateShare', methods=['POST'])
@login_required
@admin_required
def updateShare():
    g.db_connection.db_audit_share_update_by_uuid(request.form['new_share_type'],
                                                  request.form['new_share_user'],
                                                  request.form['new_share_password'],
                                                  request.form['new_share_server'],
                                                  request.form['new_share_path'],
                                                  request.form['id'])
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
