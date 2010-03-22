# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
import re

class MailSender:
    
    def __init__(self):
        f = open("login.ogame")
        info = f.read()
        self.sendTo = re.search("sendTo:\s(.*?);", info, re.M).group(1)
        self.sendFrom = re.search("sendFrom:\s(.*?);", info, re.M).group(1)
        self.senderPass = re.search("sendPass:\s(.*?);", info, re.M).group(1)
        
    def sendEmail(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sendFrom
        msg['To'] = self.sendTo
        
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.sendFrom, self.senderPass)
        mailServer.sendmail(self.sendFrom, [self.sendTo], msg.as_string())
        mailServer.quit()

if __name__ == '__main__':
    sender = MailSender()
    sender.sendEmail("Test email Subject", "A Body!")