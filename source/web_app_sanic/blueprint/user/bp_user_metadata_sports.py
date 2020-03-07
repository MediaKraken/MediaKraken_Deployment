from common import common_global
from common import common_pagination
from sanic import Blueprint

blueprint_user_metadata_sports = Blueprint('name_blueprint_user_metadata_sports',
                                           url_prefix='/user')


@blueprint_user_metadata_sports.route('/meta_sports_detail/<guid>')
@common_global.jinja_template.template('user/meta_sports_detail.html')
async def url_bp_user_metadata_sports_detail(request, guid):
    """
    Display sports detail metadata
    """
    return {
        'guid': guid,
        'data': g.db_connection.db_meta_sports_guid_by_thesportsdb(guid)
    }


@blueprint_user_metadata_sports.route('/meta_sports_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_sports_list.html')
async def url_bp_user_metadata_sports_list(request):
    """
    Display sports metadata list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for row_data in g.db_connection.db_meta_sports_list(
            offset, per_page, common_global.session['search_text']):
        media.append((row_data['mm_metadata_sports_guid'],
                      row_data['mm_metadata_sports_name']))
    common_global.session['search_page'] = 'meta_sports'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_sports_list_count(
                                                      common_global.session['search_text']),
                                                  record_name='sporting event(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return {
        'media_sports_list': g.db_connection.db_meta_sports_list(offset, per_page,
                                                                 common_global.session[
                                                                     'search_text']),
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
