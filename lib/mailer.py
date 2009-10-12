import smtplib
from email.MIMEText import MIMEText

class Mailer:
    def __init__(self, recipient, body):
        self.recipient = recipient
        self.msg = MIMEText(body)
        self.msg['Subject'] = "ELC Application Status"
        self.msg['From'] = "m50mnj1@wpo.cso.niu.edu"
        self.msg['Reply-to'] = "m50mnj1@wpo.cso.niu.edu"
        self.msg['To'] = self.recipient

    def mail_it(self):
        print self.msg.as_string()
        s = smtplib.SMTP()
        s.connect("smtp.staff.niu.edu")
        s.sendmail(
            "m50mnj1@wpo.cso.niu.edu",
            self.recipient,
            self.msg.as_string()
        )
        s.close()