





@blueprint.route('/meta_game_detail/<guid>')
@login_required
async def url_bp_user_metadata_game_detail(request, guid):
    """
    Display game metadata detail
    """
    return render_template('users/metadata/meta_game_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_by_guid(
                               guid)['gi_game_info_json'],
                           data_review=None)


@blueprint.route('/meta_game_system_list', methods=['GET', 'POST'])
@login_required
async def url_bp_user_metadata_game_system_list(request):
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
async def url_bp_user_metadata_game_system_detail(request, guid):
    """
    Display game system detail metadata
    """
    return render_template('users/metadata/meta_game_system_detail.html', guid=guid,
                           data=g.db_connection.db_meta_game_system_by_guid(guid))
