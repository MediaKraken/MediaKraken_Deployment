from sanic import Blueprint

from .public import public_content

content_mediakraken = Blueprint.group(public_content, url_prefix='/')
