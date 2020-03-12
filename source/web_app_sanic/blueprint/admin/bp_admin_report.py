import os

from common import common_global
from common import common_string
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_admin_report = Blueprint('name_blueprint_admin_report', url_prefix='/admin')


@blueprint_admin_report.route('/report_all_media')
@common_global.jinja_template.template('admin/admin_report_all_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_all_media(request):
    """
    Display all media list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media_data = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_media_known(db_connection, offset, per_page):
        media_data.append((row_data['mm_media_path'],
                           common_string.com_string_bytes2human(
                               os.path.getsize(row_data['mm_media_path']))))
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_media_known_count(
                                db_connection),
                            record_name='all media',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_report.route('/report_duplicate')
@common_global.jinja_template.template('admin/admin_report_all_duplicate_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_all_duplicate_media(request):
    """
    Display media duplication report page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_media_duplicate_count(
                                db_connection),
                            record_name='duplicate media',
                            format_total=True,
                            format_number=True,
                            )
    report_media = await request.app.db_functions.db_media_duplicate(db_connection,
                                                                     offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media': report_media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_report.route('/report_duplicate_detail/<guid>')
@common_global.jinja_template.template('admin/admin_report_duplicate_media_detail.html')
@common_global.auth.login_required
async def url_bp_admin_report_duplicate_detail(request, guid):
    """
    Display detail of duplicate list
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for media_data in await request.app.db_functions.db_media_duplicate_detail(db_connection, guid,
                                                                               offset, per_page):
        common_global.es_inst.com_elastic_index('info', {"media": media_data[
            'mm_media_ffprobe_json']})
        if media_data['mm_media_ffprobe_json'] is not None:
            for stream_data in media_data['mm_media_ffprobe_json']['streams']:
                if stream_data['codec_type'] == 'video':
                    media.append((media_data['mm_media_guid'], media_data['mm_media_path'],
                                  str(stream_data['width']) +
                                  'x' + str(stream_data['height']),
                                  media_data['mm_media_ffprobe_json']['format']['duration']))
                    break
        else:
            media.append((media_data['mm_media_guid'], media_data['mm_media_path'],
                          'NA', '999:99:99'))
    pagination = Pagination(request,
                            total=await
                            request.app.db_functions.db_media_duplicate_detail_count(db_connection,
                                                                                     guid)[0],
                            record_name='copies',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {
        'media': media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_report.route('/report_top10/<mtype>')
@common_global.jinja_template.template('admin/admin_report_top10_base.html')
@common_global.auth.login_required
async def url_bp_admin_report_top10(request, mtype):
    """
    Display top10 pages
    """
    db_connection = await request.app.db_pool.acquire()
    top10_data = None
    if mtype == '1':  # all time
        top10_data = await request.app.db_functions.db_usage_top10_alltime(db_connection)
    elif mtype == '2':  # movie
        top10_data = await request.app.db_functions.db_usage_top10_movie(db_connection)
    elif mtype == '3':  # tv show
        top10_data = await request.app.db_functions.db_usage_top10_tv_show(db_connection)
    elif mtype == '4':  # tv episode
        top10_data = await request.app.db_functions.db_usage_top10_tv_episode(db_connection)
    await request.app.db_pool.release(db_connection)
    return {'media': top10_data}


@blueprint_admin_report.route('/report_unmatched_media')
@common_global.jinja_template.template('admin/admin_report_unmatched_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_display_all_unmatched_media(request):
    """
    Display list of all unmatched media
    """
    page, per_page, offset = Pagination.get_page_args(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_media_unmatched_list_count(
                                db_connection),
                            record_name='unmatched media',
                            format_total=True,
                            format_number=True,
                            )
    unmatched_media = await request.app.db_functions.db_media_unmatched_list(db_connection,
                                                                             offset=offset,
                                                                             list_limit=per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media': unmatched_media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
