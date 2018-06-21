# -*- coding: utf-8 -*-

import json
import os
import sys

sys.path.append('..')
from quart import Blueprint, render_template, g, request, flash, \
    url_for, redirect
from flask_login import login_required

blueprint = Blueprint("admins_library", __name__,
                      url_prefix='/admin', static_folder="../static")
# need the following three items for admin check
import quart
from flask_login import current_user
from functools import wraps
from MediaKraken.extensions import (
    fpika,
)
from MediaKraken.admins.forms import LibraryAddEditForm

from common import common_config_ini
from common import common_global
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
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
        if not current_user.is_admin:
            return quart.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/library", methods=["GET", "POST"])
@blueprint.route("/library/", methods=["GET", "POST"])
@login_required
@admin_required
async def admin_library():
    """
    List all media libraries
    """
    if request.method == 'POST':
        # submit the message
        ch = fpika.channel()
        ch.basic_publish(exchange='mkque_ex', routing_key='mkque',
                         body=json.dumps({'Type': 'Library Scan'}))
        fpika.return_channel(ch)
        flash("Scheduled media scan.")
        common_global.es_inst.com_elastic_index('info', {'stuff': 'scheduled media scan'})
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_media_dir'),
                                                  record_name='library dir(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template("admin/admin_library.html",
                           media_dir=g.db_connection.db_audit_paths(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route("/library_edit", methods=["GET", "POST"])
@blueprint.route("/library_edit/", methods=["GET", "POST"])
@login_required
@admin_required
async def admin_library_edit_page():
    """
    allow user to edit lib
    """
    form = LibraryAddEditForm(await request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            if await request.form['action_type'] == 'Add':
                # check for UNC
                if await request.form['library_path'][:1] == "\\":
                    addr, share, path = common_string.com_string_unc_to_addr_path(
                        await request.form['library_path'])
                    common_global.es_inst.com_elastic_index('info',
                                                            {'smb info': addr, 'share': share,
                                                             'path': path})
                    if addr is None:  # total junk path for UNC
                        flash("Invalid UNC path.", 'error')
                        return redirect(url_for('admins_library.admin_library_edit_page'))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(addr)
                    if not smb_stuff.com_cifs_share_directory_check(share, path):
                        smb_stuff.com_cifs_close()
                        flash("Invalid UNC path.", 'error')
                        return redirect(url_for('admins_library.admin_library_edit_page'))
                    smb_stuff.com_cifs_close()
                # smb/cifs mounts
                elif await request.form['library_path'][0:3] == "smb":
                    # TODO
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(
                        ip_addr, user_name='guest', user_password='')
                    smb_stuff.com_cifs_share_directory_check(
                        share_name, dir_path)
                    smb_stuff.com_cifs_close()
                # nfs mount
                elif await request.form['library_path'][0:3] == "nfs":
                    # TODO
                    pass
                elif not os.path.isdir(await request.form['library_path']):
                    flash("Invalid library path.", 'error')
                    return redirect(url_for('admins_library.admin_library_edit_page'))
                # verify it doesn't exist and add
                if g.db_connection.db_audit_path_check(await request.form['library_path']) == 0:
                    try:
                        lib_share = await request.form['Lib_Share']
                    except:
                        lib_share = None
                    g.db_connection.db_audit_path_add(await request.form['library_path'],
                                                      await request.form['Lib_Class'], lib_share)
                    g.db_connection.db_commit()
                    return redirect(url_for('admins_library.admin_library'))
                else:
                    flash("Path already in library.", 'error')
                    return redirect(url_for('admins_library.admin_library_edit_page'))
            elif await request.form['action_type'] == 'Browse...':  # popup browse form
                pass
            # popup browse form for synology
            elif await request.form['action_type'] == 'Synology':
                pass
        else:
            flash_errors(form)
    class_list = []
    for row_data in g.db_connection.db_media_class_list():
        if row_data['mm_media_class_display']:  # flagged for display
            class_list.append(
                (row_data['mm_media_class_type'], row_data['mm_media_class_guid']))
    share_list = []
    for row_data in g.db_connection.db_audit_shares():
        share_name = row_data['mm_media_share_server'] + \
                     ":" + row_data['mm_media_share_path']
        share_list.append((share_name, row_data['mm_media_share_guid']))

    return await render_template("admin/admin_library_edit.html", form=form,
                           data_class=class_list,
                           data_share=share_list)


@blueprint.route('/library_delete', methods=["POST"])
@login_required
@admin_required
async def admin_library_delete_page():
    """
    Delete library action 'page'
    """
    g.db_connection.db_audit_path_delete(await request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint.route('/getLibraryById', methods=['POST'])
@login_required
@admin_required
async def getLibraryById():
    result = g.db_connection.db_audit_path_by_uuid(await request.form['id'])
    return json.dumps({'Id': result['mm_media_dir_guid'],
                       'Path': result['mm_media_dir_path'],
                       'Media Class': result['mm_media_dir_class_type']})


@blueprint.route('/updateLibrary', methods=['POST'])
@login_required
@admin_required
async def updateLibrary():
    g.db_connection.db_audit_path_update_by_uuid(await request.form['new_path'],
                                                 await request.form['new_class'], await request.form['id'])
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
