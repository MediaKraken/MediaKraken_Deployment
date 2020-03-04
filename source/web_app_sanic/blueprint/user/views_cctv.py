@blueprint.route('/cctv')
@login_required
def cctv():
    """
    Display cctv page
    """
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_sync_list_count(),
                                                  record_name='CCTV System(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/user_cctv.html',
                           media_sync=g.db_connection.db_sync_list(
                               offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/cctv_detail/<guid>')
@login_required
def cctv_detail(guid):
    """
    Display cctv detail
    """
    pass
