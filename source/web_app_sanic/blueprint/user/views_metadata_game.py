

@blueprint.route('/meta_game_list', methods=["GET", "POST"])
@login_required
def metadata_game_list():
    """
    Display game list metadata
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_game'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_game_software_info'),
                                                  record_name='game(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_game_list.html',
                           media_game=g.db_connection.db_meta_game_list(offset, per_page,
                                                                        session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_game_detail/<guid>')
@login_required
def metadata_game_detail(guid):
    """
    Display metadata game detail
    """
    return render_template('users/metadata/meta_game_detail.html',
                           )
