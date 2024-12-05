import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, target_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = target_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, target_email, text)
    server.quit() 