import smtplib
from email.mime.text import MIMEText
from config import Config

def send_availability_email(email, slots, participant_id):
    link_base = "http://localhost:5000/api/confirm"
    body = f"Hi,\nPlease confirm one of these slots:\n"
    for slot in slots:
        link = f"{link_base}?id={participant_id}&slot={slot}"
        body += f"- {slot}: {link}\n"
    
    msg = MIMEText(body)
    msg['Subject'] = 'Interview proposal with Mastro HR'
    msg['From'] = Config.SMTP_USERNAME
    msg['To'] = email

    with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(msg)
