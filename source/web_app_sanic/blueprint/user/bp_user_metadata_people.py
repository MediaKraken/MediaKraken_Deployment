from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint

blueprint_user_metadata_people = Blueprint('name_blueprint_user_metadata_people',
                                           url_prefix='/user')


@blueprint_user_metadata_people.route('/user_meta_person_detail/<guid>')
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_person_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_person_detail(request, guid):
    """
    Display person detail page
    """
    db_connection = await request.app.db_pool.acquire()
    person_data = await request.app.db_functions.db_meta_person_by_guid(db_connection, guid)
    if person_data['mmp_person_image'] is not None:
        try:
            person_image = person_data['mmp_person_image'] + person_data['mmp_meta']
        except:
            person_image = "/static/images/person_missing.png"
    else:
        person_image = "/static/images/person_missing.png"
    media_data = await request.app.db_functions.db_meta_person_as_seen_in(db_connection,
                                                                          person_data['mmp_id'])
    await request.app.db_pool.release(db_connection)
    return {
        'json_metadata': person_data['mmp_person_meta_json'],
        'data_person_image': person_image,
        'data_also_media': media_data,
    }


@blueprint_user_metadata_people.route('/user_meta_person_list', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_person.html')
@common_global.auth.login_required
async def url_bp_user_metadata_person_list(request):
    """
    Display person list page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    person_list = []
    db_connection = await request.app.db_pool.acquire()
    for person_data in await request.app.db_functions.db_meta_person_list(db_connection, offset,
                                                                          per_page,
                                                                          request['session'][
                                                                              'search_text']):
        common_global.es_inst.com_elastic_index('info', {'person data': person_data, 'im':
            person_data['mmp_person_image'], 'meta': person_data['mmp_meta']})
        if person_data['mmp_person_image'] is not None:
            try:
                person_image = person_data['mmp_person_image'] + person_data['mmp_meta']
            except:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
        person_list.append(
            (person_data['mmp_id'], person_data['mmp_person_name'], person_image))
    request['session']['search_page'] = 'meta_people'
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_meta_person_list_count(
                                db_connection,
                                request['session']['search_text']),
                            record_name='person',
                            format_total=True,
                            format_number=True,
                            )
    await request.app.db_pool.release(db_connection)
    return {
        'media_person': person_list,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }
