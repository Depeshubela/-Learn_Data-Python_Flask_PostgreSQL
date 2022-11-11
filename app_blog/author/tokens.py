from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired

from app_blog import app
from flask import current_app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

'''
def confirm_token(self):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    
    return serializer.dumps({'user_id': self.id},salt=app.config['SECURITY_PASSWORD_SALT'])
'''

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def reset_token(token):
   
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=86400)

'''
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)  # 驗證
    except SignatureExpired:
        #  當時間超過的時候就會引發SignatureExpired錯誤
        return False
    except BadSignature:
        #  當驗證錯誤的時候就會引發BadSignature錯誤
        return False
    return data
 '''