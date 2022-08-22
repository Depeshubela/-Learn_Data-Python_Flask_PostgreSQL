import os 


class Config:
    #pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.dirname(__file__)) + "/app_blog/static/data/data_register.sqlite"
    SECRET_KEY = b'\xb9k\xdf@\x0e\x1f(\xf2\xb0\xd0\xcb?Y\xdcN\x19G\x12e\xa8\x8b\xe5\xccS'

    #class EmailConfig:
    DEBUG=False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_DEFAULT_SENDER=('admin', 'sean940106@gmail.com')
    MAIL_MAX_EMAILS=10
    MAIL_USERNAME='sean940106@gmail.com'
    MAIL_PASSWORD='kqhedsyrohrgflcm'
    SECURITY_PASSWORD_SALT = "Liebe"