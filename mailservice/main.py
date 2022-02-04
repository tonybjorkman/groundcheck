
import sys

sys.path.append('/home/tony/code/groundcheck/flaskproject')
print(sys.path)
from db import *
from models import *
from sqlalchemy import or_
import mail
mailer = mail.Mailer()
limit=1

# get not passed controllEntries
def get_not_passed_controllEntries():
    return session.query(ControlledEntry,TestSample).filter(ControlledEntry.test_id==TestSample.id).filter(or_(TestSample.passed==False, TestSample.error==True)).filter(ControlledEntry.mail_sent==False).all()


for entry, sample in get_not_passed_controllEntries(): 
    print(entry.description)
    print(sample.test_value)
    try:
        mailer.send_mail("olle@dmail.com","Sample was:"+str(sample.test_value))
        entry.mail_sent=True
        session.commit()
    except:
        print("Failed to send mail")






