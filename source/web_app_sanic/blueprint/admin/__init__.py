from sanic import Blueprint

from .bp_admin_backup import blueprint_admin_backup
from .bp_admin_cron import blueprint_admin_cron
from .bp_admin_docker import blueprint_admin_docker
from .bp_admin_library import blueprint_admin_library
from .bp_admin_users import blueprint_admin_users

blueprint_public_content = Blueprint.group(blueprint_admin_backup,
                                           blueprint_admin_cron,
                                           blueprint_admin_docker,
                                           blueprint_admin_library,
                                           blueprint_admin_users,
                                           )
