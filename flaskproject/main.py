from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.name)

@main.route('/table')
@login_required
def table():
    return render_template('table.html',users=db.session.query(User).all())
