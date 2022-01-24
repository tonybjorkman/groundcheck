import smtplib

# Create a SMTP object
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

# Start the connection
smtpObj.starttls()

# Read username and password from file
with open('credentials.txt', 'r') as f:
    username = f.readline().strip()
    password = f.readline().strip()

# Login
smtpObj.login(username, password)

# Send the email to tony_bjorkman@hotmail.com
smtpObj.sendmail(username, 'tony_bjorkman@hotmail.com', 'Hello')

# Close the connection
smtpObj.quit()