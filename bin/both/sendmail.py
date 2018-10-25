import smtplib
from email.mime.text import MIMEText

msg = MIMEText(text)

msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP('localhost', 25)
s.login(username, password)
s.send_message(msg)
s.quit()