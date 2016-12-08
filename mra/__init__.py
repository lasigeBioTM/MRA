from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tasks import make_celery

app = Flask(__name__)
app.config.from_pyfile('../config.cfg')


celery = make_celery(app)

db = SQLAlchemy(app)

import mra.views
