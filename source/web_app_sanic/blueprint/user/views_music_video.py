
@blueprint.route('/music_video_list', methods=['GET', 'POST'])
@login_required
def user_music_video_list():
    """
    Display music video page
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'media_music_video'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_music_video_list_count(
                                                      session['search_text']),
                                                  record_name='music video(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_music_video_list.html',
                           media_person=g.db_connection.db_music_video_list(offset, per_page,
                                                                            session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/music_video_detail/<guid>')
@login_required
def user_music_video_detail(guid):
    """
    Display music video page
    """
    pass

