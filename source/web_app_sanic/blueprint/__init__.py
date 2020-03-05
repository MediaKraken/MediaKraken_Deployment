from sanic import Blueprint

from .public import blueprint_public_content
from .user import blueprint_user_content

blueprint_content_mediakraken = Blueprint.group(blueprint_public_content,
                                                blueprint_user_content,
                                                )
