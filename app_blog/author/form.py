from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError
from wtforms.fields import EmailField
from app_blog.author.model import UserRegister
from wtforms import BooleanField

class FormRegister(FlaskForm):
    """依照Model來建置相對應的Form
    
    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(2, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 50),
        validators.Email()
    ])
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')
    def validate_email(self, field):
        if UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('此信箱已被使用')

    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            raise  ValidationError('此名稱已被使用')

class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 50),
        validators.Email()
    ])

    password = PasswordField('PassWord', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Keep Logged in')

    submit = SubmitField('Log in')

class FormChangePWD(FlaskForm):
    """
    使用者變更密碼
    舊密碼、新密碼與新密碼確認
    """
    #  舊密碼
    password_old = PasswordField('Old PassWord', validators=[
        validators.DataRequired()
    ])
    #  新密碼
    password_new = PasswordField('New PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_new_confirm', message='PASSWORD NEED MATCH')
    ])
    #  新密碼確認
    password_new_confirm = PasswordField('Confirm New PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Change Password')
    
class FormResetMail(FlaskForm):
    """應用於密碼遺失申請時輸入郵件使用"""
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])
    submit = SubmitField('Send Confirm EMAIL')

    def validate_email(self, field):
        """
        驗證是否有相關的EMAIL在資料庫內，若沒有就不寄信
        """
        if not UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('No Such EMAIL, Please Check!')


class FormResetPassword(FlaskForm):
    """使用者申請遺失密碼"""
    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_confirm', message='PASSWORD NEED MATCH')
    ])
    password_confirm = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Reset Password')