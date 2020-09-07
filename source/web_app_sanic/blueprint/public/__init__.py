from sanic import Blueprint

from .bp_public_about import blueprint_public_about

blueprint_public_content = Blueprint.group(blueprint_public_about)
