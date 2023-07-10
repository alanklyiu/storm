from flask import flash, redirect, render_template, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required, login_user, logout_user

from . import auth_bp
from .forms import LoginForm
#from .. import db
from ..models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.dashboard'))
    form = LoginForm()
    """
    redirect returns a 302 header to the browser, with its Location header as the URL for its argument; render_template returns a 200, with the template of its argument returned as the content at that URL
    """
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html', form=form, title="Login")


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out.')
    return redirect(url_for('home.index'))