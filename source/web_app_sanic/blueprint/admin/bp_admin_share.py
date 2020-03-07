import json
import os

from common import common_global
from common import common_network_cifs
from common import common_pagination
from sanic import Blueprint

blueprint_admin_share = Blueprint('name_blueprint_admin_share', url_prefix='/admin')


@blueprint_admin_share.route("/share", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_share.html')
@admin_required
async def url_bp_admin_share(request):
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
    return {
        'media_dir': g.db_connection.db_audit_shares(
            offset, per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_share.route('/share_delete', methods=["POST"])
@admin_required
async def url_bp_admin_share_delete(request):
    """
    Delete share action 'page'
    """
    g.db_connection.db_audit_share_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})


@blueprint_admin_share.route("/share_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_share_edit.html')
@admin_required
async def url_bp_admin_share_edit(request):
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
                    #                        await request.form['storage_mount_path'])
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
                    return redirect(request.app.url_for('admins_share.admin_share_edit_page'))
                # verify it doesn't exit and add
                if g.db_connection.db_audit_share_check(request.form['storage_mount_path']) == 0:
                    g.db_connection.db_audit_share_add(request.form['storage_mount_type'],
                                                       request.form['storage_mount_user'],
                                                       request.form['storage_mount_password'],
                                                       request.form['storage_mount_server'],
                                                       request.form['storage_mount_path'])
                    g.db_connection.db_commit()
                    return redirect(request.app.url_for('admins_share.admin_share'))
                else:
                    flash("Share already mapped.", 'error')
                    return redirect(request.app.url_for('admins_share.admin_share_edit_page'))
            elif request.form['action_type'] == 'Browse':
                # browse for smb shares on the host network
                pass
        else:
            flash_errors(form)
    return {'form': form}
