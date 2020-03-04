
# 3d
@blueprint.route('/3D')
@login_required
def user_3d_list():
    """
    Display 3D media page
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'media_3d'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_3d_list_count(),
                                                  record_name='3D',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("users/user_3d_list.html",
                           media=g.db_connection.db_3d_list(offset, per_page,
                                                            session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination, )
