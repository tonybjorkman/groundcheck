
import sys

sys.path.append('/home/tony/code/groundcheck/flaskproject')
print(sys.path)
from db import *
from models import *
from read_settings import *
from sqlalchemy import or_
import mail
import time
mailer = mail.Mailer()
limit=1



# get not passed controllEntries
def get_not_passed_controllEntries():
    return session.query(ControlledEntry).join(TestSample). \
            filter(TestSample.passed==False). \
                filter(ControlledEntry.handled==False).all()

def get_expired_control_entries(time_now,allowed_timedelta_min):
    allowed_time=session.query(Settings).time_to_refresh
    return session.query(ControlledEntry).join(TestSample).filter(TestSample.test_time-time_now>allowed_time).filter(ControlledEntry.handled==False).all()

def get_control_errors():
    return session.query(ControlledEntry).join(TestSample). \
    filter(TestSample.error==True). \
    filter(ControlledEntry.handled==False).all()


        
def failed_test_message(entry):
    message = entry.name + ' '


def send_alarm(entry):
        print(entry.description)
        try:
            mailer.send_mail(entry.employee.manager,format_mail(entry), "Autosober Alert")
            set_entry_handled(entry)
            return True
        except:
            print("Failed to send mail. Entry not updated to 'handled' and will be sent later")
            return False

def format_mail(entry) -> str:
    if entry.test.passed:
        return "Employee entrance is OK"

    if not entry.test.error:
        return "Employee #"+entry.employee_number+" has triggered alcohol "+ \
        "alarm with "+entry.test.test_value+" as alc value on time " + \
            str(entry.test.testtime) 
    
    if entry.test.error:
        return "Test Error occured for Employee #"+entry.employee_number

def set_entry_handled(entry):
    entry.handled=True
    session.commit()

def main():
    unhandled_entries = []
    unhandled_entries.extend(get_not_passed_controllEntries())
    unhandled_entries.extend(get_expired_control_entries())
    unhandled_entries.extend(get_control_errors())
    

    for entry in unhandled_entries: 
        if send_alarm(entry):
            set_entry_handled(entry)



if __name__ == "__main__":
    main()

