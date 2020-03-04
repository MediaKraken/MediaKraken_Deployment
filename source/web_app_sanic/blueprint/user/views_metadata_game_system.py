
@blueprint.route('/meta_game_system_detail/<guid>')
@login_required
def metadata_game_system_detail(guid):
    """
    Display metadata game detail
    """
    return render_template('users/metadata/meta_game_system_detail.html',
                           )


@blueprint.route('/meta_game_system_list', methods=['GET', 'POST'])
@login_required
def metadata_game_system_list():
    """
    Display list of game system metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_game_system'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_game_system_list_count(),
                                                  record_name='game system(s)',
                                                  format_total=True,
                                                  format_number=True
                                                  )
    return render_template('users/metadata/meta_game_system_list.html',
                           media=g.db_connection.db_meta_game_system_list(offset, per_page,
                                                                          session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
