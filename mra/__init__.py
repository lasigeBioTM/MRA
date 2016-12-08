from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from tasks import make_celery


app = Flask(__name__)
app.config.from_pyfile('../config.cfg')


celery = make_celery(app)
db = SQLAlchemy(app)

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == app.config['BASIC_AUTH_USERNAME']:
        return app.config['BASIC_AUTH_PASSWORD']


import mra.views
