import os
import logging
from flask import Flask, jsonify
from flask_login import LoginManager
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.exceptions import HTTPException
from .settings import config as conf

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

config = conf[os.environ.get("FLASK_ENV", "default")]
config.init_app(app)
app.config.from_object(config)

login = LoginManager(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)

from . import routes

if __name__ == "__main__":
    app.run(host=app.config["HOST"])
