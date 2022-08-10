from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os


#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9']\
   # = 'postgresql://yuacqtdojxgkqv:28050498cf7a8c7f569598e1b9adc03b80349dbb3e0b0d91ab328aa0156524b8@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d8q79pjsluumf9'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                       #os.path.join(pjdir, 'data_register.sqlite')
                                        
app.config['SECRET_KEY']='your key'

Bootstrap(app)
db = SQLAlchemy(app)
#db.create_all()



class UserRegister(db.Model):
    """記錄使用者資料的資料表"""
    __tablename__ = 'UserRgeisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)





@app.route('/register', methods=['GET', 'POST'])
def register():
    from form import FormRegister
    #from model import UserRegister
    form =FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success Thank You'
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()