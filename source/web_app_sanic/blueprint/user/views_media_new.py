

@blueprint.route('/new_media', methods=['GET', 'POST'])
@login_required
async def url_bp_user_newmedia_page(request):
    """
    Display new media
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'new_media'
    media_data = []
    for media_file in g.db_connection.db_read_media_new(offset, per_page, session['search_text'],
                                                        days_old=7):
        media_data.append(
            (media_file['mm_media_class_type'],
             media_file['mm_media_name'], None))
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_read_media_new_count(
                                                      session['search_text'],
                                                      days_old=7),
                                                  record_name='new media',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_newmedia.html',
                           media=media_data,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

