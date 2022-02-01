from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class TestSample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_value = db.Column(db.Numeric(10,2))
    description = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    test_time = db.Column(db.DateTime)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'))
    instrument = db.relationship('Instrument')

class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    ip = db.Column(db.String(15))

class ControlledEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    entry = db.Column(db.DateTime)
    test_id = db.Column(db.Integer, db.ForeignKey('test_sample.id'))
    test = db.relationship('TestSample')

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    value = db.Column(db.String(1000))
    changed = db.Column(db.DateTime)