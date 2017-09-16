# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_caching import Cache
Cache = Cache()

from flask_debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask_pika import Pika as FPika
fpika = FPika()
