from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '^$%#%^*&*(()*(^&^%%$#$%##$@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/bookmanagement?charset=utf8mb4'  # % quote('Quyet@1511')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)

cloudinary.config(cloud_name='dj9dngnhr', api_key='491212336282522', api_secret='cwizoJCHMD98oek4qDzhl6KPvy4')

@babel.localeselector
def load_locale():
    return 'vi'


