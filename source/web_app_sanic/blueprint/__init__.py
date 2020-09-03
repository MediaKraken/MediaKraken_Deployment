from sanic import Blueprint

from .admin import blueprint_admin_content
from .error import blueprint_error_content
from .public import blueprint_public_content
from .user import blueprint_user_content

blueprint_content_mediakraken = Blueprint.group(blueprint_admin_content,
                                                blueprint_error_content,
                                                blueprint_public_content,
                                                blueprint_user_content,
                                                )
