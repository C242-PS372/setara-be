import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.config import config
from src.routes.routes import routes
from src.utils.db import db

# Flask App Initialization
app = Flask(__name__)
app.config.from_object(config.settings[os.environ.get('APPLICATION_ENV', 'default')])
app.register_blueprint(get_swaggerui_blueprint('/api/docs', '/static/api-docs.json',), url_prefix='/api/docs')

CORS(app)


jwt = JWTManager(app)

# Database and migration initalization
db.init_app(app)
migrate = Migrate(app, db)

# Flask API Initialization
routes.init_app(app)