from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)  
login.login_view = 'login'

mail = Mail(app)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

#  很重要，一定要放這邊
from app_blog.author import view
