from sanic import Blueprint

from .bp_error import blueprint_error

blueprint_error_content = Blueprint.group(blueprint_error)
