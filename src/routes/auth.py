from flask_restful import Api
from src.utils.errors import errors
from src.controllers.user import UserController
from src.controllers.auth import SignInController, SignUpController, SelfAuth

from src.middleware.jwt_auth import jwt_auth

auth_routes = Api(
    catch_all_404s=True,
    errors=errors,
    prefix='/auth'
)

auth_routes.add_resource(SignInController, '/sign-in')
auth_routes.add_resource(SignUpController, '/sign-up')
auth_routes.add_resource(SelfAuth, '/self')