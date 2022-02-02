from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .db import Session
from .models import TestSample, User, Instrument
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
    return render_template('table.html',
    users=Session.query(User).all(),
    instruments=Session.query(Instrument).all(),
    samples=Session.query(TestSample))

@main.route('/table', methods=["POST"])
@login_required
def table_post():
    name = request.form.get('name')
    ip = request.form.get('ip')
    description = request.form.get('description')
    print('Name '+name)
    i = Instrument(name=name, ip=ip, description=description)
    Session.add(i)
    Session.commit()
    return redirect(url_for('main.table'))

@main.route('/table/del/instrument/<int:id>')
@login_required
def table_delete_instrument(id):
    print("Deleted instrument"+str(id))
    i = Session.query(Instrument).filter_by(id=id).first()
    Session.delete(i)
    Session.commit()
    return redirect(url_for('main.table'))

@main.route('/table/del/user/<int:id>')
@login_required
def table_delete_user(id):
    print("Deleted userid:"+str(id))
    i = Session.query(User).filter_by(id=id).first()
    Session.delete(i)
    Session.commit()
    return redirect(url_for('main.table'))