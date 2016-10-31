"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request, current_app, jsonify, redirect, url_for
from flask_login import login_required
from flask_login import current_user
#from flask_table import Table, Col, create_table
from flask_paginate import Pagination
blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_file
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


def flash_errors(form):
    """
    Display each error on top of form
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


@blueprint.route("/")
@login_required
def members():
    """
    Display main members page
    """
    resume_list = []
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_read_media_new_count(7),
                                                  record_name='new and hot',
                                                  format_total=True,
                                                  format_number=True,
                                                 )
    return render_template("users/members.html", data_resume_media=resume_list,
                           data_new_media=g.db_connection.db_read_media_new(7, offset, per_page),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.route('/server')
@blueprint.route('/server/')
@login_required
def server():
    """
    Display server page
    """
    return render_template("users/user_server.html")


@blueprint.route('/search/<name>/')
@blueprint.route('/search/<name>')
@login_required
def search(name):
    """
    Search media
    """
    sql = 'select count(*) from users where name like ?'
    args = ('%{}%'.format(name), )
    g.cur.execute(sql, args)
    try:
        total = g.cur.fetchone()[0]
    except:
        total = 0
    page, per_page, offset = common_pagination.get_page_items()
    sql = 'select * from users where name like %s limit {}, {}'
    g.cur.execute(sql.format(offset, per_page), args)
    users = g.cur.fetchall()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=total,
                                                  record_name='Users',
                                                 )
    return render_template('users/user_report_all_known_media_video.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                          )


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    pass


@blueprint.teardown_request
def teardown_request(exception):
    """
    Executes after each request
    """
    pass
