# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

if __name__ == '__main__':
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # fp = open(textfile, 'rb')
    # Create a text/plain message
    msg = MIMEText("what")
    #fp.close()
    
    me = "*@*.com"# me == the sender's email address
    myPW = "*"
    you = "*@*.com"# you == the recipient's email address
    msg['Subject'] = 'The contents of %s' % "theMessage"
    msg['From'] = me
    msg['To'] = you
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(me, myPW)
    mailServer.sendmail(me, [you], msg.as_string())
    mailServer.quit()
