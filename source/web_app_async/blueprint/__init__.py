from sanic import Blueprint

from .public import blueprint_public_content

blueprint_content_mediakraken = Blueprint.group(blueprint_public_content, url_prefix='/')
