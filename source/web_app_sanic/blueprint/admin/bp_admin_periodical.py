import json
import uuid

from common import common_global
from sanic import Blueprint

blueprint_admin_periodical = Blueprint('name_blueprint_admin_periodical', url_prefix='/admin')


@blueprint_admin_periodical.route('/admin_periodical_add', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_admin/bss_admin_periodical_add.html')
async def url_bp_admin_periodical_add(request):
    """
    Display periodical add page
    """
    if request.method == 'POST':
        class_uuid = common_global.DLMediaType.Publication_Book.value
        for book_item in request.form['book_list'].split('\r'):
            if len(book_item) > 2:
                media_id = uuid.uuid4()
                db_connection = await request.app.db_pool.acquire()
                await request.app.db_functions.db_media_insert(media_id, None,
                                                               class_uuid,
                                                               None, None, None,
                                                               db_connection=db_connection)
                await request.app.db_functions.db_download_insert('Z', 0,
                                                                  json.dumps({'MediaID': media_id,
                                                                              'Path': None,
                                                                              'ClassID': class_uuid,
                                                                              'Status': None,
                                                                              'MetaNewID': str(
                                                                                  uuid.uuid4()),
                                                                              'ProviderMetaID': book_item.strip()}),
                                                                  db_connection=db_connection)
                await request.app.db_pool.release(db_connection)
        return redirect(request.app.url_for('admins.admin_books_add'))
    form = BookAddForm(request, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    return {
        'form': form
    }
