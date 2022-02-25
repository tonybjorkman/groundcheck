
from email import message
import sys

sys.path.append('/home/tony/code/groundcheck/flaskproject')
print(sys.path)
from db import *
from models import *
from read_settings import *
from sqlalchemy import or_
import mail
from datetime import datetime
from read_settings import Settings
from message import MessageFactory
msg_factory=MessageFactory()
mailer = mail.Mailer()
limit=1

settings = Settings()







class EntryFinder():


    def find_unhandled():
        return session.query(ControlledEntry).join(TestSample).filter(ControlledEntry.handled==False).all()

    def getError():
        return super().find_unhandled.filter(TestSample.error==True)

    #function to calculate how long in hours it has been since a date and time
    def delta(entry):
        now = datetime.now()
        diff = now - entry.test_time
        return diff.seconds/3600 + diff.days*24

    def getTimedout(self):
        allowed_time = settings.time_to_test_first_time
        unhandled = super().find_unhandled
        expired = []
        for entry in unhandled:
            if self.delta(entry)>allowed_time:
                expired.extend(entry)
        return expired
    
    def getFailed():
        return super().find_unhandled.filter(TestSample.passed==False)



class EntryAlarmHandler():
    def __init__(self, mailer):
        self.mailer=mailer
        self.finder=EntryFinder()


    def handleTimedout(self, finder, mailer, sender):
        to_do = finder.getTimedout()
        for item in to_do:
            self.send_alarm(msg_factory, item, 'timedout', sender)

    def handleErrors(self, finder, mailer, sender):
        to_do = finder.getError()
        for item in to_do:
            self.send_alarm(msg_factory, item, 'error', sender)


    def handleFailed(self, finder, mailer, sender):
        to_do = finder.getFailed()
        for item in to_do:
            self.send_alarm(msg_factory, item, 'failed', sender)


    def set_entry_handled(entry):
        entry.handled=True
        session.commit()


    def send_alarm(self, msg_factory, entry, type, sender):
        print(entry.description)
        try:
            mailer.send_mail(entry.employee.manager, "Autosober alert message", msg_factory.createEmployeeMessage(entry, type, sender))
            self.set_entry_handled(entry)
            return True
        except:
            print("Failed to send mail. Entry not updated to 'handled' and will be sent later")
            return False

    

# def format_mail(entry) -> str:
#     if entry.test.passed:
#         return "Employee entrance is OK"

#     if not entry.test.error:
#         return "Employee #"+entry.employee_number+" has triggered alcohol "+ \
#         "alarm with "+entry.test.test_value+" as alc value on time " + \
#             str(entry.test.testtime) 
    
#     if entry.test.error:
#         return "Test Error occured for Employee #"+entry.employee_number
