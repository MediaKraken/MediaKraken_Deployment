# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

import redis

from MediaKraken import public, user, admins
from MediaKraken.assets import assets
from MediaKraken.extensions import (
    bcrypt,
    db,
    login_manager,
)
from MediaKraken.settings import ProdConfig
from flask import Flask, render_template
from flask_kvsession import KVSessionExtension
from flask_uwsgi_websocket import GeventWebSocket
from simplekv.memory.redisstore import RedisStore


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    KVSessionExtension(RedisStore(redis.StrictRedis(host='mkredis')), app)
    app.config.from_object(config_object)
    app.config['UPLOAD_FOLDER'] = '/mediakraken/uploads'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    websocket = GeventWebSocket(app)
    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    # load up public bps
    app.register_blueprint(public.views.blueprint)
    # load up user bps
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(user.views_3d.blueprint)
    app.register_blueprint(user.views_cctv.blueprint)
    app.register_blueprint(user.views_chromecast.blueprint)
    app.register_blueprint(user.views_class.blueprint)
    app.register_blueprint(user.views_comic_reader.blueprint)
    app.register_blueprint(user.views_games.blueprint)
    app.register_blueprint(user.views_hardware.blueprint)
    app.register_blueprint(user.views_hardware_hue.blueprint)
    app.register_blueprint(user.views_home_media.blueprint)
    app.register_blueprint(user.views_images.blueprint)
    app.register_blueprint(user.views_internet.blueprint)
    app.register_blueprint(user.views_media_new.blueprint)
    app.register_blueprint(user.views_metadata_album.blueprint)
    app.register_blueprint(user.views_metadata_game.blueprint)
    app.register_blueprint(user.views_metadata_game_system.blueprint)
    app.register_blueprint(user.views_metadata_movie.blueprint)
    app.register_blueprint(user.views_metadata_music_video.blueprint)
    app.register_blueprint(user.views_metadata_people.blueprint)
    app.register_blueprint(user.views_metadata_periodical.blueprint)
    app.register_blueprint(user.views_metadata_sports.blueprint)
    app.register_blueprint(user.views_metadata_tv.blueprint)
    app.register_blueprint(user.views_movie.blueprint)
    app.register_blueprint(user.views_movie_collection.blueprint)
    app.register_blueprint(user.views_movie_genre.blueprint)
    app.register_blueprint(user.views_music.blueprint)
    app.register_blueprint(user.views_music_video.blueprint)
    app.register_blueprint(user.views_periodicals.blueprint)
    app.register_blueprint(user.views_playback.blueprint)
    app.register_blueprint(user.views_queue.blueprint)
    app.register_blueprint(user.views_search.blueprint)
    app.register_blueprint(user.views_sports.blueprint)
    app.register_blueprint(user.views_sync.blueprint)
    app.register_blueprint(user.views_tv.blueprint)
    app.register_blueprint(user.views_tv_live.blueprint)
    # load up admin bps
    app.register_blueprint(admins.views.blueprint)
    app.register_blueprint(admins.views_backup.blueprint)
    app.register_blueprint(admins.views_chromecasts.blueprint)
    app.register_blueprint(admins.views_cron.blueprint)
    app.register_blueprint(admins.views_docker.blueprint)
    app.register_blueprint(admins.views_game_metadata.blueprint)
    app.register_blueprint(admins.views_library.blueprint)
    app.register_blueprint(admins.views_link.blueprint)
    app.register_blueprint(admins.views_media_import.blueprint)
    app.register_blueprint(admins.views_messages.blueprint)
    app.register_blueprint(admins.views_reports.blueprint)
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
