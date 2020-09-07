"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
"""

import math

from common import common_internationalization


def com_pagination_page_calc(request):
    page = int(request.args.get('page', 1))
    offset = (page * int(request.ctx.session['per_page'])) - int(request.ctx.session['per_page'])
    return page, offset


def com_pagination_boot_html(page, url, item_count=0,
                             client_items_per_page=30, format_number=True):
    """
    Set items and count per page
    """
    # if everything fits on one page, don't paginate.
    if item_count < client_items_per_page:
        return '', 0
    # start pagination calculations
    pages = math.ceil(item_count / client_items_per_page)
    pagination_links = '<ul class="pagination">'
    # only do previous if not on first page
    if page > 1:
        if format_number:
            page_number = common_internationalization.com_inter_number_format(page - 1)
        else:
            page_number = str(page - 1)
        pagination_links += '<li class="page-item">' \
                            '<a class="page-link" href="' + url + '?page=' + page_number \
                            + '" aria-label="Previous">' \
                              '<span aria-hidden="true">&laquo;</span>' \
                              '<span class="sr-only">Previous</span>' \
                              '</a>' \
                              '</li>'
    # if less than ten pages, just display all the pages
    if pages < 10:
        build_start = 1
        build_stop = pages
    else:
        build_start = page
        build_stop = page + 10
        if build_stop > pages:
            build_stop = pages
    for ndx in range(build_start, build_stop):
        if format_number:
            page_number = common_internationalization.com_inter_number_format(ndx)
        else:
            page_number = str(ndx)
        pagination_links += '<li class="page-item"><a class="page-link"' \
                            ' href="' + url + '?page=' + page_number + '">' \
                            + page_number + '</a></li>'
    # only do next if not on last page
    if page < pages:
        if format_number:
            page_number = common_internationalization.com_inter_number_format(page + 1)
        else:
            page_number = str(page + 1)
        pagination_links += '<li class="page-item">' \
                            '<a class="page-link" href="' + url + '?page=' + page_number \
                            + '" aria-label="Next">' \
                              '<span aria-hidden="true">&raquo;</span>' \
                              '<span class="sr-only">Next</span>' \
                              '</a>' \
                              '</li>'
    pagination_links += '</ul>'
    return pagination_links
