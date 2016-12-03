from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

app = Flask(__name__)
app.config.from_pyfile('../config.cfg')


celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
)

db = SQLAlchemy(app)

import mra.views
