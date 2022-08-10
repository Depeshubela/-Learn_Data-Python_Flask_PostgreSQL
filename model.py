from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import os




#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9']\
   or 'sqlite:///' + os.path.join(pjdir,'data.sqlite')

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9']\
   #= 'postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                       #os.path.join(pjdir, 'data_register.sqlite')




db = SQLAlchemy(app)

class UserReister(db.Model):
    """記錄使用者資料的資料表"""
    __tablename__ = 'UserRgeisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)

db.create_all()