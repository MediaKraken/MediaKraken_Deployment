ALLOWED_EXTENSIONS = {'py', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

outside_ip = None


def admin_required(fn):
    """
    Admin check
    """

    @wraps(fn)
    @login_required
    def decorated_view(*args, **kwargs):
        common_global.es_inst.com_elastic_index('info', {"admin access attempt by":
                                                             user.id})
        if not current_user.is_admin:
            return flask.abort(403)  # access denied
        return fn(*args, **kwargs)

    return decorated_view


@blueprint.route("/chart_browser")
@login_required
@admin_required
async def url_bp_admin_chart_browser():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,
                               25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None,
                              None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66,
                          58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9,
                              9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route("/chart_client_usage")
@login_required
@admin_required
async def url_bp_admin_chart_client_usage(request):
    line_chart = pygal.Line()
    line_chart.title = 'Client usage'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Theater', [None, None, 0, 16.6,
                               25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Roku', [None, None, None, None,
                            None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('Web', [85.8, 84.6, 84.7, 74.5, 66,
                           58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('iOS', [14.2, 15.4, 15.3, 8.9, 9,
                           10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Android', [14.2, 15.4, 15.3, 8.9,
                               9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart.add('Tizen', [14.2, 15.4, 15.3, 8.9,
                             9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    line_chart = line_chart.render(is_unicode=True)
    return render_template("admin/chart/chart_base_usage.html", line_chart=line_chart)


@blueprint.route('/', defaults={'path': ''}, endpoint='listdir')
@blueprint.route('/<path:path>/list', endpoint='listdirpath')
@login_required
@admin_required
async def url_bp_admin_listdir(request, path):
    """
    Local file browser
    """

    def gather_fileinfo(path, ospath, filename):
        osfilepath = os.path.join(ospath, filename)
        if os.path.isdir(osfilepath) and not filename.startswith('.'):
            return {'type': 'd', 'filename': filename,
                    'link': url_for('admins.admin_listdir',
                                    path=os.path.join(path, filename))}
        else:
            return {'type': 'f', 'filename': filename,
                    'fullpath': os.path.join(path, filename)}

    try:
        path = os.path.normpath(path)
        ospath = os.path.join('/', path)
        files = list(
            map(partial(gather_fileinfo, path, ospath), os.listdir(ospath)))
        files = list(filter(lambda file: file is not None, files))
        files.sort(key=lambda i: (
                                         i['type'] == 'file' and '1' or '0') + i[
                                     'filename'].lower())
        return render_template('admin/admin_fs_browse.html',
                               files=files,
                               parent=os.path.dirname(path),
                               path=path)
    except IOError:
        abort(404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
@admin_required
async def url_bp_admin_upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_handle = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file_handle.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file_handle and allowed_file(file_handle.filename):
            filename = secure_filename(file_handle.filename)
            file_handle.save(os.path.join('/mediakraken/uploads', filename))
            return redirect(request.app.url_for('uploaded_file',
                                                filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
