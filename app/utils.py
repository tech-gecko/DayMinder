from flask_mail import Message
from . import mail

def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.body = body
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
