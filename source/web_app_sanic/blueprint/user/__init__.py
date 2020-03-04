from sanic import Blueprint

from .bp_user_homepage import blueprint_user_homepage

blueprint_user_content = Blueprint.group(blueprint_user_homepage)
