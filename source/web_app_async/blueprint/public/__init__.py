from sanic import Blueprint

from .bp_about import blueprint_public_about
from .bp_homepage import blueprint_public_homepage

blueprint_public_content = Blueprint.group(blueprint_public_about,
                                           blueprint_public_homepage)
