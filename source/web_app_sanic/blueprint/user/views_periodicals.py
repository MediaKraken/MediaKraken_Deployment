
# books
@blueprint.route('/books', methods=['GET', 'POST'])
@login_required
def user_books_list():
    """
    Display books page
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'media_periodicals'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_media_book_list_count(
                                                      session['search_text']),
                                                  record_name='periodical(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template("users/user_books_list.html",
                           media=g.db_connection.db_media_book_list(offset, per_page,
                                                                    session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/book_detail/<guid>')
@login_required
def user_books_detail(guid):
    """
    Display books page
    """
    pass

