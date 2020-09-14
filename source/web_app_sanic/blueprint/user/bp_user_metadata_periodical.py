from common import common_global
from common import common_isbn
from common import common_pagination_bootstrap
from sanic import Blueprint

blueprint_user_metadata_periodical = Blueprint('name_blueprint_user_metadata_periodical',
                                               url_prefix='/user')


@blueprint_user_metadata_periodical.route('/user_meta_periodical', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_periodical.html')
@common_global.auth.login_required
async def url_bp_user_metadata_periodical(request):
    """
    Display periodical list page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    item_list = []
    db_connection = await request.app.db_pool.acquire()
    for item_data in await request.app.db_functions.db_meta_periodical_list(db_connection, offset,
                                                                            int(request.ctx.session[
                                                                                    'per_page']),
                                                                            request.ctx.session[
                                                                                'search_text']):
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'person data': item_data})
        item_image = "img/missing_icon.jpg"
        item_list.append((item_data['mm_metadata_book_guid'],
                          item_data['mm_metadata_book_name'], item_image))
    request.ctx.session['search_page'] = 'meta_periodical'
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/user/user_meta_periodical',
                                                                      item_count=await request.app.db_functions.db_meta_periodical_list_count(
                                                                          db_connection,
                                                                          request.ctx.session[
                                                                              'search_text']),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media_person': item_list,
        'pagination_links': pagination,
    }


@blueprint_user_metadata_periodical.route('/user_meta_periodical_detail/<guid>')
@common_global.jinja_template.template('bss_user/metadata/bss_user_metadata_periodical_detail.html')
@common_global.auth.login_required
async def url_bp_user_metadata_periodical_detail(request, guid):
    """
    Display periodical detail page
    """
    db_connection = await request.app.db_pool.acquire()
    json_metadata = await request.app.db_functions.db_meta_periodical_by_uuid(db_connection, guid)
    await request.app.db_pool.release(db_connection)
    try:
        data_name = json_metadata['mm_metadata_book_json']['title']
    except KeyError:
        data_name = 'NA'
    try:
        data_isbn = common_isbn.com_isbn_mask(json_metadata['mm_metadata_book_json']['isbn10'])
    except KeyError:
        data_isbn = 'NA'
    try:
        data_overview = json_metadata['mm_metadata_book_json']['summary']
    except KeyError:
        data_overview = 'NA'
    try:
        data_author = json_metadata['mm_metadata_book_json']['author_data'][0]['name']
    except KeyError:
        data_author = 'NA'
    try:
        data_publisher = json_metadata['mm_metadata_book_json']['publisher_name']
    except KeyError:
        data_publisher = 'NA'
    try:
        data_pages = json_metadata['mm_metadata_book_json']['physical_description_text']
    except KeyError:
        data_pages = 'NA'
    return {
        'data_name': data_name,
        'data_isbn': data_isbn,
        'data_overview': data_overview,
        'data_author': data_author,
        'data_publisher': data_publisher,
        'data_pages': data_pages,
        'data_item_image': "img/missing_icon.jpg",
    }
