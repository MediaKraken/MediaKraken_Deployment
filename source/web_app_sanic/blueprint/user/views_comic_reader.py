
@blueprint.route('/comic_view/<guid>')
@login_required
async def url_bp_user__comic_view(request, guid):
    """
    Display image comic view
    """
    return render_template("users/user_comic_view.html",
                           comic_data=await database_base_async.db_media_path_by_uuid(db_connection, guid))

