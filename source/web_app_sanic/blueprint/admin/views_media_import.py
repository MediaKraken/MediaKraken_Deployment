
def admin_required(fn):
    """
    Admin check
    """

    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             current_user.get_id()})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/mediaimport", methods=["GET", "POST"])
@login_required
@admin_required
async def url_bp_admin_media_import(request):
    """
    Import media
    """
    media_data = []
    media_file_list = common_file.com_file_dir_list('/mediakraken/mnt/incoming',
                                                    filter_text=None,
                                                    walk_dir=True,
                                                    skip_junk=True,
                                                    file_size=True,
                                                    directory_only=False)
    if media_file_list is not None:
        for media_file in media_file_list:
            media_data.append((media_file[0], media_file[1]))
    return render_template("admin/admin_media_import.html",
                           media_dir=media_data,
                           )

