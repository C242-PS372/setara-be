from flask_restful import Api

from src.utils.errors import errors
from src.middleware.jwt_auth import jwt_auth
from src.controllers.user import UserController
from src.routes.auth import auth_routes

routes = Api(
    catch_all_404s=True,
    errors=errors,
    prefix='/api'
)

routes.add_resource(auth_routes)

routes.add_resource(UserController, '/user')