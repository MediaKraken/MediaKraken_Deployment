from sanic import Blueprint

from .bp_about import bp_about
from .bp_homepage import bp_homepage

public_content = Blueprint.group(bp_about, bp_homepage, url_prefix='/public')
