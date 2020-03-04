

@blueprint.route('/games', methods=['GET', 'POST'])
@login_required
def user_games_list():
    """
    Display games page
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'media_games'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.
                                                  db_meta_game_system_list_count(),
                                                  record_name='game system(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("users/user_game_list.html",
                           media=g.db_connection.db_meta_game_system_list(offset, per_page,
                                                                          session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/games_detail/<guid>', methods=['GET', 'POST'])
@login_required
def user_games_detail(guid):
    """
    Display game detail page
    """
    return render_template("users/user_game_detail.html")


@blueprint.route('/meta_game_detail/<guid>')
@login_required
def metadata_game_detail(guid):
    """
    Display game metadata detail
    """
    return render_template('users/metadata/meta_game_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_by_guid(
                               guid)['gi_game_info_json'],
                           data_review=None)


@blueprint.route('/meta_game_system_list', methods=['GET', 'POST'])
@login_required
def metadata_game_system_list():
    """
    Display game system metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.
                                                  db_meta_game_system_list_count(),
                                                  record_name='Game Systems',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_game_system_list.html',
                           media_game_system=g.db_connection.db_meta_game_system_list(offset,
                                                                                      per_page,
                                                                                      session[
                                                                                          'search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_system_detail/<guid>')
@login_required
def metadata_game_system_detail(guid):
    """
    Display game system detail metadata
    """
    return render_template('users/metadata/meta_game_system_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_system_by_guid(guid))
