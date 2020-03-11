from sanic import Blueprint

from .bp_admin import blueprint_admin
from .bp_admin_backup import blueprint_admin_backup
from .bp_admin_cron import blueprint_admin_cron
from .bp_admin_docker import blueprint_admin_docker
from .bp_admin_hardware import blueprint_admin_hardware
from .bp_admin_hardware_chromecast import blueprint_admin_hardware_chromecast
from .bp_admin_hardware_tvtuner import blueprint_admin_hardware_tvtuner
from .bp_admin_library import blueprint_admin_library
from .bp_admin_report import blueprint_admin_report
from .bp_admin_users import blueprint_admin_users

blueprint_admin_content = Blueprint.group(blueprint_admin,
                                          blueprint_admin_backup,
                                          blueprint_admin_cron,
                                          blueprint_admin_docker,
                                          blueprint_admin_hardware,
                                          blueprint_admin_hardware_chromecast,
                                          blueprint_admin_library,
                                          blueprint_admin_report,
                                          blueprint_admin_hardware_tvtuner,
                                          blueprint_admin_users,
                                          )
