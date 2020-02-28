from sanic import Blueprint
from sanic import response

blueprint_public_homepage = Blueprint('name_blueprint_public_homepage', url_prefix='/public')


@blueprint_public_homepage.route('/home', methods=['GET', 'POST'])
async def url_bp_homepage(request):
    """
    Display home page
    """
    if 'search_text' in session:
        pass
    else:
        session['search_text'] = None
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user, False)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form, user=current_user)
    #return await response.file('./web_app_async/templates/public/home.html')
