from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_sports = Blueprint('name_blueprint_user_sports', url_prefix='/user')


# list of spoting events
@blueprint_user_sports.route("/sports", methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_sports.html')
@common_global.auth.login_required
async def url_bp_user_sports(request):
    """
    Display sporting events page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    for row_data in g.db_connection.db_media_sports_list(
            common_global.DLMediaType.Sports.value,
            offset, per_page, common_global.session['search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    common_global.session['search_page'] = 'media_sports'
    pagination = Pagination(request,
                            total=g.db_connection.db_media_sports_list_count(
                                common_global.session['search_text']),
                            record_name='sporting event(s)',
                            format_total=True,
                            format_number=True,
                            )
    return {'media': media,
            'page': page,
            'per_page': per_page,
            'pagination': pagination,
            }


@blueprint_user_sports.route("/sports_detail/<guid>", methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_sports_detail.html')
@common_global.auth.login_required
async def url_bp_user_sports_detail(request, guid):
    """
    Display sports detail page
    """
    # poster image
    try:
        if json_metadata['LocalImages']['Poster'] is not None:
            data_poster_image = json_metadata['LocalImages']['Poster']
        else:
            data_poster_image = None
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return {
        'data': g.db_connection.db_metathesportsdb_select_guid(guid),
        'data_poster_image': data_poster_image,
        'data_background_image': data_background_image,
    }
