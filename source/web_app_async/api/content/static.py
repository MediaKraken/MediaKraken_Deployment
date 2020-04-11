# api/content/static.py
from sanic import Blueprint

static = Blueprint('content_static', url_prefix='/static')
