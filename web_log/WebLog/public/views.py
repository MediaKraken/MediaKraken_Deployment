# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import (Blueprint, request, render_template, flash, url_for, redirect, session)
from flask_login import login_user, login_required, logout_user
from flask_login import current_user

from WebLog.extensions import login_manager
from WebLog.user.models import User
from WebLog.public.forms import LoginForm
from WebLog.user.forms import RegisterForm
from WebLog.utils import flash_errors
import logging # pylint: disable=W0611

# this fixes the login issue!!!!!!!!!!!!!!!!!!!!!!!!!
#blueprint = Blueprint('public', __name__, url_prefix='/public', static_folder="../static")
blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """
    Display home page
    """
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
    return render_template("public/home.html", form=form,user=current_user)


@blueprint.route('/logout/')
@login_required
def logout():
    """
    Logout user and clear their session
    """
    logout_user()
    session.clear()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    """
    Display registration form
    """
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    """
    Display about page
    """
    return render_template("public/about.html")
