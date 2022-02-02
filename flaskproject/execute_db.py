from ipaddress import ip_address
from models import User, Instrument, TestSample
from db import engine, session
from datetime import datetime

for u in session.query(User).all():
    print(u)

'''i = Instrument(name='Exhalitics v2', description='A new instrument',ip="192.168.0.1")
session.add(i)
session.commit()'''

for u in session.query(Instrument).all():
    print(u)

ts = TestSample(test_value=1.23, description="A new test sample", test_time=datetime.now(), user_id=1, instrument_id=1)
session.add(ts)
session.commit()