import json
import os

from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network_cifs
from common import common_pagination_bootstrap
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.bss_form_share import BSSShareAddEditForm

blueprint_admin_share = Blueprint('name_blueprint_admin_share', url_prefix='/admin')


@blueprint_admin_share.route("/admin_share", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_share.html')
@common_global.auth.login_required
async def url_bp_admin_share(request):
    """
    List all share/mounts
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_share',
                                                                      item_count=await request.app.db_functions.db_table_count(
                                                                          table_name='mm_media_share',
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    media_share = await request.app.db_functions.db_share_list(offset, int(request.ctx.session[
                                                                               'per_page']),
                                                               db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'media_dir': media_share,
        'pagination_links': pagination,
    }


@blueprint_admin_share.route('/admin_share_by_id', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_share_by_id(request):
    db_connection = await request.app.db_pool.acquire()
    result = await request.app.db_functions.db_share_update_by_uuid(request.form['id'],
                                                                    db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'Id': result['mm_share_dir_guid'],
                       'Path': result['mm_share_dir_path']})


@blueprint_admin_share.route('/admin_share_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_share_delete(request):
    """
    Delete share action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_share_delete(request.form['id'], db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_admin_share.route("/admin_share_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_share_edit.html')
@common_global.auth.login_required
async def url_bp_admin_share_edit(request):
    """
    allow user to edit share
    """
    form = BSSShareAddEditForm(request)
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'stuff': 'hereeditshare'})
    if request.method == 'POST':
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'stuff': 'herepost'})
        if form.validate_on_submit():
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'action':
                                                                                     request.form[
                                                                                         'action_type']})
            if request.form['action_type'] == 'Add':
                await common_logging_elasticsearch_httpx.com_es_httpx_post_async(
                    message_type='info',
                    message_text={
                        'type': request.form[
                            'storage_mount_type']})
                # check for UNC
                if request.form['storage_mount_type'] == "unc":
                    #                    addr, share, path = common_string.com_string_unc_to_addr_path(\
                    #                        await request.form['storage_mount_path'])
                    #                    if addr is None: # total junk path for UNC
                    #                        request['flash']("Invalid UNC path.", 'error')
                    #                        return redirect(url_for('admins_share.admin_share_edit_page'))
                    #                    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text= {'stuff':'unc info: %s %s %s' % (addr, share, path))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(request.form['storage_mount_server'],
                                               user_name=request.form['storage_mount_user'],
                                               user_password=request.form['storage_mount_password'])
                    #                    if not smb_stuff.com_cifs_share_directory_check(\
                    #                            request.form['storage_mount_server'], \
                    #                            request.form['storage_mount_path']):
                    #                        smb_stuff.com_cifs_close()
                    #                        request['flash']("Invalid UNC path.", 'error')
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
                    request['flash']("Invalid share path.", 'error')
                    return redirect(request.app.url_for('admins_share.admin_share_edit_page'))
                # verify it doesn't exit and add
                db_connection = await request.app.db_pool.acquire()
                if await request.app.db_functions.db_share_check(request.form[
                                                                     'storage_mount_path'],
                                                                 db_connection) == 0:
                    await request.app.db_functions.db_share_add(request.form[
                                                                    'storage_mount_type'],
                                                                request.form[
                                                                    'storage_mount_user'],
                                                                request.form[
                                                                    'storage_mount_password'],
                                                                request.form[
                                                                    'storage_mount_server'],
                                                                request.form[
                                                                    'storage_mount_path'],
                                                                db_connection)
                    await request.app.db_pool.release(db_connection)
                    return redirect(request.app.url_for('admins_share.admin_share'))
                else:
                    request['flash']("Share already mapped.", 'error')
                    await request.app.db_pool.release(db_connection)
                    return redirect(request.app.url_for('admins_share.admin_share_edit_page'))
            elif request.form['action_type'] == 'Browse':
                # browse for smb shares on the host network
                pass
        else:
            flash_errors(form)
    return {'form': form}


@blueprint_admin_share.route('/admin_share_update', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_share_update(request):
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_share_update_by_uuid(request.form['new_share_type'],
                                                           request.form['new_share_user'],
                                                           request.form['new_share_password'],
                                                           request.form['new_share_server'],
                                                           request.form['new_share_path'],
                                                           request.form['id'],
                                                           db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})
