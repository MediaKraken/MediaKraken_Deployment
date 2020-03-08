from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_people = Blueprint('name_blueprint_user_metadata_people',
                                           url_prefix='/user')


@blueprint_user_metadata_people.route('/meta_person_detail/<guid>')
@common_global.jinja_template.template('user/meta_person_detail.html')
async def url_bp_user_metadata_person_detail(request, guid):
    """
    Display person detail page
    """
    person_data = g.db_connection.db_meta_person_by_guid(guid)
    if person_data['mmp_person_image'] is not None:
        if 'themoviedb' in person_data['mmp_person_image']['Images']:
            try:
                person_image = person_data['mmp_person_image']['Images']['themoviedb'].replace(
                    '/mediakraken/web_app/MediaKraken', '') + person_data['mmp_meta']
            except:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
    else:
        person_image = "/static/images/person_missing.png"
    return {
        'json_metadata': person_data['mmp_person_meta_json'],
        'data_person_image': person_image,
        'data_also_media': g.db_connection.db_meta_person_as_seen_in(
            person_data['mmp_id']),
    }


@blueprint_user_metadata_people.route('/meta_person_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/meta_person_list.html')
async def url_bp_user_metadata_person_list(request):
    """
    Display person list page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    person_list = []
    for person_data in g.db_connection.db_meta_person_list(offset, per_page,
                                                           common_global.session['search_text']):
        common_global.es_inst.com_elastic_index('info', {'person data': person_data, 'im':
            person_data['mmp_person_image'], 'meta': person_data['mmp_meta']})
        if person_data['mmp_person_image'] is not None:
            if 'themoviedb' in person_data['mmp_person_image']['Images']:
                try:
                    person_image = person_data['mmp_person_image']['Images']['themoviedb'].replace(
                        '/mediakraken/web_app/MediaKraken', '') + person_data['mmp_meta']
                except:
                    person_image = "/static/images/person_missing.png"
            else:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
        person_list.append(
            (person_data['mmp_id'], person_data['mmp_person_name'], person_image))
    common_global.session['search_page'] = 'meta_people'
    pagination = Pagination(request,
                            total=g.db_connection.db_meta_person_list_count(
                                common_global.session['search_text']),
                            record_name='person',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_person': person_list,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
