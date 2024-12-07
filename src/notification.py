import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.logging_config import logger

def send_email(sender_email, sender_password, target_email, subject, body):
    try:
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
        
        logger.info("Email sent successfully", extra={
            'to_email': target_email,
            'subject': subject
        })
    except smtplib.SMTPException as e:
        logger.error("SMTP error occurred", extra={
            'to_email': target_email,
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise
    except Exception as e:
        logger.error("Failed to send email", extra={
            'to_email': target_email,
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise 