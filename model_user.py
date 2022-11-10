from flask import Flask
#  from flask.ext.sqlalchemy import SQLAlchemy<--新版取消了
from flask_sqlalchemy import SQLAlchemy
import os


#  取得目前文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置sqlite檔案路徑
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    #os.path.join(pjdir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pevhejgfzgogsk:265bf34b2b464bdb35a128b4241346a28d600c6741a3b151a05e15aab0b0c762@    ec2-52-70-86-157.compute-1.amazonaws.com:5432/dfcoadhf47jppl'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #  設置關聯，relationship設置於一對多的『一』

    def __repr__(self):
        return '<User %r>' % self.username
    
    def __repr__(self):
        return 'contact_style:%s, contact_context:%s' % \
            (self.contact_style, self.contact_context)

db.drop_all()