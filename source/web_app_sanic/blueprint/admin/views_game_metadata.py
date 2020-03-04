

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


@blueprint.route("/game_metadata", methods=["GET", "POST"])
@login_required
@admin_required
def game_metadata():
    """
    Game metadata stats and update screen
    """
    if request.method == 'POST':
        docker_inst = common_docker.CommonDocker()
        docker_inst.com_docker_run_game_data()
    data_mame_version = None
    return render_template("admin/admin_games_metadata.html",
                           data_mame_version=data_mame_version,
                           )

