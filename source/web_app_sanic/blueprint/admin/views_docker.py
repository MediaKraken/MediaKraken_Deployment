

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


@blueprint.route("/docker_stat")
@login_required
@admin_required
def docker_stat():
    """
    Docker statistics including swarm
    """
    docker_inst = common_docker.CommonDocker()
    # it returns a dict, not a json
    docker_info = docker_inst.com_docker_info()
    common_global.es_inst.com_elastic_index('info', {'Docker info': docker_info})
    if 'Managers' not in docker_info['Swarm'] or docker_info['Swarm']['Managers'] == 0:
        docker_swarm = "Cluster not active"
    else:
        docker_swarm = docker_inst.com_docker_swarm_inspect()[
            'JoinTokens']['Worker']
    return render_template("admin/admin_docker.html",
                           data_host=docker_info,
                           data_swam=docker_swarm
                           )

