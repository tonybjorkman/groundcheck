#from . import db
#from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String,Numeric, ForeignKey, DateTime, Boolean 
from sqlalchemy.orm import relationship

Base = declarative_base()
hugo = "olle"

class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True) 
    employee_number = Column(Integer)
    manager = Column(String(255))

# Does not have employeeID on it since
# it will only be saved if connected to 
# an ControlledEntry which has it.
class TestSample(Base):
    __tablename__ = 'test_sample'
    id = Column(Integer, primary_key=True)
    test_value = Column(Numeric(10,2))
    passed = Column(Boolean)
    error = Column(Boolean)
    description = Column(String(1000))
    test_time = Column(DateTime)
    instrument_id = Column(Integer, ForeignKey('instrument.id'))
    instrument = relationship('Instrument')

class Instrument(Base):

    __tablename__ = 'instrument'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    description = Column(String(1000))
    ip = Column(String(15))

class ControlledEntry(Base):

    __tablename__ = 'controlled_entry'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    employee = relationship('Employee')
    entry_time = Column(DateTime)
    test_id = Column(Integer, ForeignKey('test_sample.id'))
    test = relationship('TestSample')
    handled = Column(Boolean)
    description = Column(String(1000))

class Settings(Base):

    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    value = Column(String(1000))
    changed = Column(DateTime)