"""Flask application factory for the Accounts service"""
from flask import Flask
from service import config

app = Flask(__name__)
app.config.from_object(config)

from service import routes, models  # noqa: E402,F401

models.init_db(app)
