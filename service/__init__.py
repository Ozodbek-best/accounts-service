"""Flask application factory for the Accounts service"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service import config

app = Flask(__name__)
app.config.from_object(config)

# Security headers (Talisman) and CORS policies
talisman = Talisman(app, force_https=False)
CORS(app)

from service import routes, models  # noqa: E402,F401

models.init_db(app)
