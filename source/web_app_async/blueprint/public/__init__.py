from sanic import Blueprint

from .bp_about import blueprint_public_about
from .bp_homepage import bp_homepage

blueprint_public_content = Blueprint.group(blueprint_public_about,
                                           bp_homepage, url_prefix='/public')
