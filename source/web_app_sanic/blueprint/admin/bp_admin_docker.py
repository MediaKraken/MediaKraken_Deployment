from common import common_docker
from common import common_global
from common import common_logging_elasticsearch_httpx
from sanic import Blueprint

blueprint_admin_docker = Blueprint('name_blueprint_admin_docker', url_prefix='/admin')


@blueprint_admin_docker.route("/admin_docker_stat")
@common_global.jinja_template.template('bss_admin/bss_admin_docker.html')
@common_global.auth.login_required
async def url_bp_admin_docker_stat(request):
    """
    Docker statistics including swarm
    """
    docker_inst = common_docker.CommonDocker()
    # it returns a dict, not a json
    docker_info = docker_inst.com_docker_info()
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'Docker info': docker_info})
    if 'Managers' not in docker_info['Swarm'] or docker_info['Swarm']['Managers'] == 0:
        docker_swarm = "Cluster not active"
    else:
        docker_swarm = docker_inst.com_docker_swarm_inspect()[
            'JoinTokens']['Worker']
    return {
        'data_host': docker_info,
        'data_swam': docker_swarm,
    }
