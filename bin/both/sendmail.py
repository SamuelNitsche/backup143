import smtplib
from email.mime.text import MIMEText
from bin.both.dbconfig import dbconf

def mail(to, subject, text):
    msg = MIMEText(text)

    msg['Subject'] = subject
    msg['From'] = dbconf('smtp_username')
    msg['To'] = to

    if(dbconf('smtp_usessl') == 1):
        s = smtplib.SMTP_SSL(dbconf('smtp_server'), dbconf('smtp_port'))
    elif(dbconf('smtp_usetls') == 1):
        s = smtplib.SMTP(dbconf('smtp_server'), dbconf('smtp_port'))
        s.starttls()
    else:
        s = smtplib.SMTP(dbconf('smtp_server'), dbconf('smtp_port'))
    s.login(dbconf('smtp_username'), dbconf('smtp_password'))
    s.send_message(msg)
    s.quit()