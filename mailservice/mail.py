import smtplib

from flask import session
from read_settings import *
from email.message import EmailMessage

settings=Settings()

class Mailer:



    def __init__(self,debug=True) -> None:
        # Create a SMTP object
        self.debug = debug
        if debug:
            self.smtpObj = smtplib.SMTP('localhost', 1025)
        else:
            self.smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

    def login(self):
        # Start the connection
        if not self.debug:
            self.smtpObj.starttls()
            username = settings.server_user
            password = settings.server_pass
            
            # # Read username and password from file
            # with open('credentials.txt', 'r') as f:
            #     username = f.readline().strip()
            #     password = f.readline().strip()
            
            # Login
            self.smtpObj.login(username, password)

    def send_mail(self, to, title, msg):
        try: 
            sender = EmailMessage()
            emailtext = "From: Autosober Alert " + settings.server_address + \
                "\nTo: " + to + "\n" + title + " has occurred \n \n" \
                    +msg

            print("sending mail :"+msg)
            self.smtpObj.sendmail(settings.server_user, to, emailtext) 
        except smtplib.SMTPException: 
            print("Error: unable to send email")


    def close(self):
        # Close the connection
        self.smtpObj.quit()


if __name__ == '__main__':
    mailer = Mailer()
    mailer.login()
    mailer.send_mail("hello","world")
    mailer.close()