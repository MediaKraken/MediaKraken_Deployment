"""
The pagination for the flask server webserver
"""

from flask import request, current_app
from flask_paginate import Pagination


def get_css_framework():
    """
    Determine framework
    """
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap4')


def get_link_size():
    """
    Determine link size for page
    """
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    """
    Determine to show single or multiple
    """
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_page_items(client_items_per_page=30):
    """
    Set items and count per page
    """
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = current_app.config.get('PER_PAGE', client_items_per_page)
    else:
        per_page = int(per_page)
    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(**kwargs):
    """
    Return pagination headers for flask
    """
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )
