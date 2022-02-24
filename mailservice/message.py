from models import *

#the basic foramtting of an email
class BaseMessage():
    def __init__(self, sender, to, subject, msg):
        self.recipient = to
        self.text="""From: """+ sender +"""
        To: """ + to + """
        Subject: """ + subject + """

        """ + msg

#the foramtting of an instrument alert
class InstrumentMessage(BaseMessage):
    def __init__(self, sender, to, subject, msg, instr):
        self.instrumentId = instr
        msg = "Instrument message: Instrument " + instr + " had an error. " + msg
        super.__init__(sender, to, subject, msg)


#the formatting of an employee entry alert
class EmployeeMessage(BaseMessage):
    def __init__(self, sender, to, subject, msg, alc_value, description):
        self.alc_value = alc_value
        self.description = description
        msg = "Employee test message: " + msg
        super.__init__(sender, to, subject, msg)



class MessageFactory():
    
    def errorMessage(entry):
        return "Employee " + entry.employee.employee_number + " had an error when using instrument " + entry.test.instrument.instrument_name + " at " + str(entry.test.test_time) + "."
    def timedoutMessage(entry):
        return str(entry.employee.employee_number) + " did not submit a test within the time limit after entering at " + str(entry.test.test_time) + "."
    def failedMessage(entry):
        return entry.employee.employee_number + " has triggered an alcohol alarm with a value of " + entry.test.test_value + " at " + str(entry.test.test_time) + ". " + \
            "The test is characterised as "+ entry.test.description


    def createInstrumentMessage(instrument, sender):
        to = 'admin'
        msg = 'Instrument: ' + instrument.name +', Id: '+instrument.id + ', Ip: ' + instrument.ip + ' is not responding.'
        subject = 'Instrument alert message'
        return InstrumentMessage(sender, to, subject, msg, instrument.id)



    def createEmployeeMessage(self, entry, type, sender):
        msg=''
        subject='Autosober alert message'
        to = entry.employee.manager
        alc_value = entry.test_value
        if type == 'error':
            msg = self.errorMessage(entry)
        elif type == 'timedout':
            msg = self.timedoutMessage(entry)
        elif type == 'failed':
            msg = self.failedMessage(entry)
        else:
            msg = "Controlled Entry: \nTime: " + entry.test.test_time + \
                "Employee: " + entry.employee.employee_number + \
                    "Instrument: " + entry.test.instrument.instrument_name +\
                        "Test result: " + entry.test.test_value + ", " + entry.test.description
            subject == 'Autosober information message'
        
        return EmployeeMessage(sender, to, subject, msg, alc_value)
