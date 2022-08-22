from threading import Thread
from flask import  render_template
from flask_mail import Message
from app_blog import mail,app

def send_async_email(app, msg):
    """
    利用多執行緒來處理郵件寄送
    :param app: 實作Flask的app
    :param msg: 實作Message的msg
    :return:
    """
    with app.app_context():
        mail.send(msg)


#  調整一下send_mail，將內容調整為樣板名稱template
def send_mail(sender, recipients, subject,  **kwargs):
    """
    sender:的部份可以考慮透過設置default
    recipients:記得要list格式
    subject:是郵件主旨
    template:樣板名稱
    **kwargs:參數
    """
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    msg.html = render_template('author/mail/welcome.html', **kwargs)

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr