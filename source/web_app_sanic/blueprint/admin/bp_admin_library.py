import json
import os

from common import common_global
from common import common_network_cifs
from common import common_network_pika
from common import common_string
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.forms import LibraryAddEditForm

blueprint_admin_library = Blueprint('name_blueprint_admin_library', url_prefix='/admin')


@blueprint_admin_library.route("/library", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_library.html')
@common_global.auth.login_required
async def url_bp_admin_library(request):
    """
    List all media libraries
    """
    common_global.es_inst.com_elastic_index('info', {'lib': request.method})
    if request.method == 'POST':
        common_global.es_inst.com_elastic_index('info', {'lib': request.form})
        if "scan" in request.form:
            # submit the message
            common_network_pika.com_net_pika_send({'Type': 'Library Scan'},
                                                  rabbit_host_name='mkstack_rabbitmq',
                                                  exchange_name='mkque_ex',
                                                  route_key='mkque')
            request['flash']('Scheduled media scan.', 'success')
            common_global.es_inst.com_elastic_index('info', {'stuff': 'scheduled media scan'})
    db_connection = await request.app.db_pool.acquire()
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                                                                'mm_media_dir'),
                            record_name='library dir(s)',
                            format_total=True,
                            format_number=True,
                            )
    return_media = []
    for row_data in await request.app.db_functions.db_library_paths(db_connection, offset,
                                                                    per_page):
        return_media.append((row_data['mm_media_dir_path'],
                             row_data['mm_media_class_guid'],
                             row_data['mm_media_dir_last_scanned'],
                             common_global.DLMediaType.row_data['mm_media_class_guid'].name,
                             row_data['mm_media_dir_guid']))
    await request.app.db_pool.release(db_connection)
    return {
        'media_dir': return_media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_library.route('/library_by_id', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_library_by_id(request):
    db_connection = await request.app.db_pool.acquire()
    result = await request.app.db_functions.db_library_path_by_uuid(db_connection,
                                                                    request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'Id': result['mm_media_dir_guid'],
                       'Path': result['mm_media_dir_path'],
                       'Media Class': result['mm_media_dir_class_type']})


@blueprint_admin_library.route('/library_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_library_delete(request):
    """
    Delete library action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_library_path_delete(db_connection, request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_admin_library.route("/library_edit", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_library_edit.html')
@common_global.auth.login_required
async def url_bp_admin_library_edit(request):
    """
    allow user to edit lib
    """
    form = LibraryAddEditForm(request.form)
    db_connection = await request.app.db_pool.acquire()
    if request.method == 'POST':
        if form.validate_on_submit():
            if request.form['action_type'] == 'Add':
                # check for UNC
                if request.form['library_path'][:1] == "\\":
                    addr, share, path = common_string.com_string_unc_to_addr_path(
                        request.form['library_path'])
                    common_global.es_inst.com_elastic_index('info',
                                                            {'smb info': addr, 'share': share,
                                                             'path': path})
                    if addr is None:  # total junk path for UNC
                        request['flash']('Invalid UNC path.', 'error')
                        return redirect(
                            request.app.url_for('admins_library.admin_library_edit_page'))
                    smb_stuff = common_network_cifs.CommonCIFSShare()
                    smb_stuff.com_cifs_connect(addr)
                    if not smb_stuff.com_cifs_share_directory_check(share, path):
                        smb_stuff.com_cifs_close()
                        request['flash']("Invalid UNC path.", 'error')
                        return redirect(
                            request.app.url_for('admins_library.admin_library_edit_page'))
                    smb_stuff.com_cifs_close()
                # TODO these should be mounted under mkmount on docker host
                # which will break docker swarm....when master moves
                # # smb/cifs mounts
                # elif request.form['library_path'][0:3] == "smb":
                #     # TODO
                #     smb_stuff = common_network_cifs.CommonCIFSShare()
                #     smb_stuff.com_cifs_connect(
                #         ip_addr, user_name='guest', user_password='')
                #     smb_stuff.com_cifs_share_directory_check(
                #         share_name, dir_path)
                #     smb_stuff.com_cifs_close()
                # # nfs mount
                # elif request.form['library_path'][0:3] == "nfs":
                #     pass
                elif not os.path.isdir(os.path.join('/mediakraken/mnt',
                                                    request.form['library_path'])):
                    request['flash']("Invalid library path.", 'error')
                    return redirect(request.app.url_for('admins_library.admin_library_edit_page'))
                # verify it doesn't exist and add
                if await request.app.db_functions.db_library_path_check(db_connection, request.form[
                    'library_path']) == 0:
                    try:
                        lib_share = request.form['Lib_Share']
                    except:
                        lib_share = None
                    await request.app.db_functions.db_library_path_add(db_connection,
                                                                       request.form[
                                                                           'library_path'],
                                                                       request.form[
                                                                           'Lib_Class'],
                                                                       lib_share)
                    return redirect(request.app.url_for('admins_library.admin_library'))
                else:
                    request['flash']("Path already in library.", 'error')
                    return redirect(request.app.url_for('admins_library.admin_library_edit_page'))
            elif request.form['action_type'] == 'Browse...':  # popup browse form
                pass
            # popup browse form for synology
            elif request.form['action_type'] == 'Synology':
                pass
        else:
            flash_errors(form)
    share_list = []
    for row_data in await request.app.db_functions.db_share_list(db_connection):
        share_name = row_data['mm_media_share_server'] + \
                     ":" + row_data['mm_media_share_path']
        share_list.append((share_name, row_data['mm_media_share_guid']))
    await request.app.db_pool.release(db_connection)
    return {
        'form': form,
        'data_class': ((common_global.DLMediaType.Movie.name,
                        common_global.DLMediaType.Movie.value),
                       (common_global.DLMediaType.TV.name,
                        common_global.DLMediaType.TV.value),
                       (common_global.DLMediaType.Music.name,
                        common_global.DLMediaType.Music.value),
                       (common_global.DLMediaType.Sports.name,
                        common_global.DLMediaType.Sports.value),
                       (common_global.DLMediaType.Game.name,
                        common_global.DLMediaType.Game.value),
                       (common_global.DLMediaType.Publication.name,
                        common_global.DLMediaType.Publication.value),
                       (common_global.DLMediaType.Picture.name,
                        common_global.DLMediaType.Picture.value),
                       (common_global.DLMediaType.Anime.name,
                        common_global.DLMediaType.Anime.value),
                       (common_global.DLMediaType.Adult.name,
                        common_global.DLMediaType.Adult.value)),
        'data_share': share_list,
    }


@blueprint_admin_library.route('/library_update', methods=['POST'])
@common_global.auth.login_required
async def url_bp_admin_library_update(request):
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_library_path_update_by_uuid(db_connection,
                                                                  request.form['new_path'],
                                                                  request.form['new_class'],
                                                                  request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})
