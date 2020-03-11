@blueprint.route("/game_metadata", methods=["GET", "POST"])
@login_required
@admin_required
async def url_bp_game_metadata(request):
    """
    Game metadata stats and update screen
    """
    data_mame_version = None
    return render_template("admin/admin_games_metadata.html",
                           data_mame_version=data_mame_version,
                           )
