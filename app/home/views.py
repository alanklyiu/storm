from flask import render_template
from flask_login import login_required

from . import home_bp


@home_bp.route('/')
def index():
    return render_template('home/index.html', title="Welcome")


@home_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html', title="Dashboard")