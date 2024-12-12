import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.config import config
from src.routes.routes import routes
from src.utils.db import db
from src.utils.predict_model import PredictModel
from src.models.user import User
from src.models.company import Company
from src.models.job_listing import JobListing
from src.models.job_type import JobType
from src.models.job_application import JobApplication
from src.models.job_recommendation import JobRecommendation

# Flask App Initialization
app = Flask(__name__)
app.config.from_object(config.settings[os.environ.get('APPLICATION_ENV', 'default')])

# Model init
PredictModel._instance

app.register_blueprint(get_swaggerui_blueprint('/api/docs', '/static/api-docs.json',), url_prefix='/api/docs')

CORS(app)


jwt = JWTManager(app)

# Database and migration initalization
db.init_app(app)
migrate = Migrate(app, db)

# Flask API Initialization
routes.init_app(app)