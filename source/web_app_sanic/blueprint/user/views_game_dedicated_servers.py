
@blueprint.route('/game_servers', methods=['GET', 'POST'])
@login_required
async def url_bp_user__game_server_list(request):
    """
    Display game server page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.
                                                  db_game_server_list_count(),
                                                  record_name='game servers(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("users/user_game_dedicated_servers.html",
                           media=g.db_connection.db_game_server_list(offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

