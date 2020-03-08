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
    for row_data in g.db_connection.db_known_media(offset, per_page):
        media_data.append((row_data['mm_media_path'],
                           common_string.com_string_bytes2human(
                               os.path.getsize(row_data['mm_media_path']))))
    pagination = Pagination(request,
                            total=g.db_connection.db_known_media_count(),
                            record_name='all media',
                            format_total=True,
                            format_number=True,
                            )
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
    pagination = Pagination(request,
                            total=g.db_connection.db_media_duplicate_count(),
                            record_name='duplicate media',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_media_duplicate(
            offset, per_page),
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
    for media_data in g.db_connection.db_media_duplicate_detail(guid, offset, per_page):
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
                            total=g.db_connection.
                            db_media_duplicate_detail_count(guid)[0],
                            record_name='copies',
                            format_total=True,
                            format_number=True,
                            )
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
    top10_data = None
    if mtype == '1':  # all time
        top10_data = g.db_connection.db_usage_top10_alltime()
    elif mtype == '2':  # movie
        top10_data = g.db_connection.db_usage_top10_movie()
    elif mtype == '3':  # tv show
        top10_data = g.db_connection.db_usage_top10_tv_show()
    elif mtype == '4':  # tv episode
        top10_data = g.db_connection.db_usage_top10_tv_episode()
    return {'media': top10_data}


@blueprint_admin_report.route('/report_unmatched_media')
@common_global.jinja_template.template('admin/admin_report_unmatched_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_display_all_unmatched_media(request):
    """
    Display list of all unmatched media
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=g.db_connection.db_unmatched_list_count(),
                            record_name='unmatched media',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media': g.db_connection.db_unmatched_list(
            offset=offset, list_limit=per_page),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
