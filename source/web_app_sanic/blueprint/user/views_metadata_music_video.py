

@blueprint.route('/meta_music_video_list', methods=['GET', 'POST'])
@login_required
async def url_bp_user_metadata_music_video_list(request):
    """
    Display metadata music video
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_music_video'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_music_video_count(
                                                      None, session['search_text']),
                                                  record_name='music video(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_music_video_list.html',
                           media=g.db_connection.db_meta_music_video_list(offset, per_page,
                                                                          session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_music_video_detail/<guid>')
@login_required
async def url_bp_user_metadata_music_video_detail(request, guid):
    """
    Display metadata music video detail
    """
    return render_template('users/metadata/meta_music_video_detail.html',
                           media=g.db_connection.db_meta_music_video_detail_uuid(guid))

