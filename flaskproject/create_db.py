import os
os.remove('db.sqlite')
#run from parent dir with 
# python3 flaskproject/create_db.py
from re import U
from models import * 
from db import engine,Session
from datetime import datetime


def load_test_data():
    u = User(name='test',email="test",password="test")
    i = Instrument(name="Exhalitics 1",description="test",ip="666")
    e = Employee(employee_number=101, manager="nr1@manager.com")
    e2 = Employee(employee_number=102, manager="nr2@manager.com")
    e3 = Employee(employee_number=103, manager="nr3@manager.com")
    e4 = Employee(employee_number=104, manager="nr4@manager.com")
    e5 = Employee(employee_number=105, manager="nr4@manager.com")
    Session.add_all([u,i,e,e2,e3,e4,e5])
    Session.commit()
    longbefore = datetime(1999, 1, 1, 0, 0)
    midnight = datetime(2000, 1, 2, 0, 0)
    midnight_15 = datetime(2000, 1, 2, 0, 15)

    ts1 = TestSample(test_value=1.0,passed=False,error=False,description="drunk entry",test_time=longbefore,instrument_id=i.id)
    ts2 = TestSample(test_value=0.0,passed=True,error=False,description="ok entry",test_time=midnight_15,instrument_id=i.id)
    ts3 = TestSample(test_value=0.0,passed=True,error=True,description="error entry",test_time=midnight_15,instrument_id=i.id)
    ts4 = TestSample(test_value=0.5,passed=True,error=False,description="ok but some alcohol entry",test_time=midnight_15,instrument_id=i.id)
    ts5 = TestSample(test_value=1.0,passed=False,error=False,description="drunk entry",test_time=midnight_15,instrument_id=i.id)

    Session.add_all([ts1,ts2,ts3,ts4,ts5])
    Session.commit()

    ce1 = ControlledEntry(employee_id=e.id, description="Tested handled w Failed",  entry_time=longbefore,  test_id=ts1.id, handled=True)
    ce2 = ControlledEntry(employee_id=e.id, description="Tested unhandled w OK",  entry_time=midnight,    test_id=ts2.id, handled=False)
    ce3 = ControlledEntry(employee_id=e2.id, description="Tested unhandled w ERROR", entry_time=midnight,    test_id=ts3.id, handled=False)
    ce4 = ControlledEntry(employee_id=e3.id, description="Tested unhandled w OK some alc", entry_time=midnight_15, test_id=ts4.id, handled=False)
    ce5 = ControlledEntry(employee_id=e4.id, description="Tested unhandled w Drunk",  entry_time=midnight,  test_id=ts5.id, handled=False)
    ce6 = ControlledEntry(employee_id=e5.id, description="not tested unhandled expired", entry_time=longbefore, handled=False)
    Session.add_all([ce1,ce2,ce3,ce4,ce5,ce6])
    Session.commit()

Base.metadata.create_all(bind=engine)
load_test_data()
