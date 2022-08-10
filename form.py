from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.fields import EmailField
from model import UserReister
from wtforms import ValidationError

class FormRegister(FlaskForm):
    """依照Model來建置相對應的Form
    
    password2: 用來確認兩次的密碼輸入相同
    """
    username = StringField('使用者名稱', validators=[
        validators.DataRequired(),
        validators.Length(3, 30)
    ])
    email = EmailField('信箱[', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('再次輸入密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('確認送出')

    def validate_email(self, field):
        if UserReister.query.filter_by(email=field.data).first():
            raise ValidationError('此信箱已被使用')

    def validate_username(self, field):
        if UserReister.query.filter_by(username=field.data).first():
            raise  ValidationError('此名稱已被使用')