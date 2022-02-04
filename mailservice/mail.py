import smtplib

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
            # Read username and password from file
            with open('credentials.txt', 'r') as f:
                username = f.readline().strip()
                password = f.readline().strip()
            # Login
            self.smtpObj.login(username, password)

    def send_mail(self, to, msg):
        print("sending mail :"+msg)
        self.smtpObj.sendmail("sender@msg.com", to, msg) 

    def close(self):
        # Close the connection
        self.smtpObj.quit()


if __name__ == '__main__':
    mailer = Mailer()
    mailer.login()
    mailer.send_mail("hello","world")
    mailer.close()