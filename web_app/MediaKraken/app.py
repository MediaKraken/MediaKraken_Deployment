# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Flask, render_template, g
from flask_moment import Moment
#from flaskext.uploads import (UploadSet, configure_uploads, IMAGES, UploadNotAllowed)
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from MediaKraken.settings import ProdConfig
from MediaKraken.assets import assets
from MediaKraken.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
)
from MediaKraken import public, user, admins
#from common import common_celery
from flask.ext.pika import Pika as FPika


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    KVSessionExtension(RedisStore(redis.StrictRedis(host='mkredis')), app)
    app.config.from_object(config_object)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg']
#    app.config['UPLOADED_PHOTOS_DEST'] = '/tmp/testuploadext'
#    upload_user_image = UploadSet('user_image', IMAGES)
#    upload_poster_image = UploadSet('user_poster', IMAGES)
#    configure_uploads(app, photos)
    g.fpika = FPika(app)
    moment = Moment(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    # load up user bps
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(user.views_3d.blueprint)
    app.register_blueprint(user.views_cctv.blueprint)
    app.register_blueprint(user.views_chromecast.blueprint)
    app.register_blueprint(user.views_class.blueprint)
    app.register_blueprint(user.views_games.blueprint)
    app.register_blueprint(user.views_images.blueprint)
    app.register_blueprint(user.views_internet.blueprint)
    app.register_blueprint(user.views_movie.blueprint)
    app.register_blueprint(user.views_movie_collection.blueprint)
    app.register_blueprint(user.views_movie_genre.blueprint)
    app.register_blueprint(user.views_music.blueprint)
    app.register_blueprint(user.views_music_video.blueprint)
    app.register_blueprint(user.views_periodicals.blueprint)
    app.register_blueprint(user.views_person.blueprint)
    app.register_blueprint(user.views_playback.blueprint)
    app.register_blueprint(user.views_reports.blueprint)
    app.register_blueprint(user.views_sports.blueprint)
    app.register_blueprint(user.views_sync.blueprint)
    app.register_blueprint(user.views_tv.blueprint)
    app.register_blueprint(user.views_tv_live.blueprint)
    app.register_blueprint(admins.views.blueprint)
    # load up admin bps
    app.register_blueprint(admins.views.blueprint)
    app.register_blueprint(admins.views_backup.blueprint)
    app.register_blueprint(admins.views_chromecasts.blueprint)
    app.register_blueprint(admins.views_cron.blueprint)
    app.register_blueprint(admins.views_docker.blueprint)
    app.register_blueprint(admins.views_library.blueprint)
    app.register_blueprint(admins.views_link.blueprint)
    app.register_blueprint(admins.views_share.blueprint)
    app.register_blueprint(admins.views_transmission.blueprint)
    app.register_blueprint(admins.views_tvtuners.blueprint)
    app.register_blueprint(admins.views_users.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
