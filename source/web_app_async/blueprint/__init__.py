from sanic import Blueprint

from .public import blueprint_public_content

content_mediakraken = Blueprint.group(blueprint_public_content, url_prefix='/')
