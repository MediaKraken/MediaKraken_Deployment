

@blueprint.route("/queue", methods=['GET', 'POST'])
@login_required
def user_queue_page():
    """
    Display queue page
    """
    page, per_page, offset = common_pagination.get_page_items()
    # TODO union read all four.....then if first "group"....add header in the html
    session['search_page'] = 'user_media_queue'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_web_tvmedia_list_count(
                                                      None, None, session['search_text']),
                                                  record_name='queue',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_queue.html',
                           media=g.db_connection.db_meta_queue_list(current_user.get_id(), offset,
                                                                    per_page,
                                                                    session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

