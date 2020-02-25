from sanic import Blueprint

from .admin import admin
from .public import public_content

content_mediakraken = Blueprint.group(admin, public_content, url_prefix='/')
