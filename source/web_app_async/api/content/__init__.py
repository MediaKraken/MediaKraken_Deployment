# api/content/__init__.py
from sanic import Blueprint

from .static import static
from .authors import authors

content = Blueprint.group(static, authors, url_prefix='/content')
