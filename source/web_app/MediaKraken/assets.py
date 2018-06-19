# -*- coding: utf-8 -*-

from flask_assets import Bundle, Environment

css = Bundle(
    "bootstrap/css/bootstrap.min.css",
    "css/style.min.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "js/jquery.min.js",
    "bootstrap/js/bootstrap.min.js",
    "js/plugins.min.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
