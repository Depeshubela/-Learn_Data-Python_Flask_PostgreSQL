from flask_mail import Message

from app_blog import mail,app


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=['AFD3456789LE@gmail.com'],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)