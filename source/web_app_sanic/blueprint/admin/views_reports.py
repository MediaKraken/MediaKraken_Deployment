


@blueprint.route('/report_duplicate')
@login_required
def report_display_all_duplicates():
    """
    Display media duplication report page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_duplicate_count(),
                                                  record_name='duplicate media',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/reports/report_all_duplicate_media.html',
                           media=g.db_connection.db_media_duplicate(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_duplicate_detail/<guid>')
@login_required
def report_display_all_duplicates_detail(guid):
    """
    Display detail of duplicate list
    """
    page, per_page, offset = common_pagination.get_page_items()
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
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.
                                                  db_media_duplicate_detail_count(guid)[0],
                                                  record_name='copies',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/reports/report_all_duplicate_media_detail.html', media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_all')
@login_required
def report_display_all_media():
    """
    Display all media list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media_data = []
    for row_data in g.db_connection.db_known_media(offset, per_page):
        media_data.append((row_data['mm_media_path'],
                           common_string.com_string_bytes2human(
                               os.path.getsize(row_data['mm_media_path']))))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_known_media_count(),
                                                  record_name='all media',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/reports/report_all_media.html', media=media_data,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_known_video')
@login_required
def report_display_all_media_known_video():
    """
    Display list of all matched video
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_media_list_count(
                                                      common_global.DLMediaType.Movie.value),
                                                  record_name='known video(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/reports/report_all_known_media_video.html',
                           media=g.db_connection.db_web_media_list(
                               common_global.DLMediaType.Movie.value,
                               list_type='movie', list_genre='All', list_limit=per_page,
                               group_collection=False,
                               offset=offset, include_remote=True,
                               search_text=None),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_unmatched_media')
@login_required
def report_display_all_unmatched_media():
    """
    Display list of all unmatched media
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_unmatched_list_count(),
                                                  record_name='unmatched media',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('admin/reports/report_unmatched_media.html',
                           media=g.db_connection.db_unmatched_list(
                               offset=offset, list_limit=per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/report_top10/<mtype>')
@login_required
def report_top10(mtype):
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
    return render_template('admin/reports/report_top10_base.html', media=top10_data)


