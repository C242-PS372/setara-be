from flask_restful import Api
from src.utils.errors import errors
from src.controllers.user import UserController
from src.controllers.auth import SignInController, SignUpController, SelfAuth
from src.controllers.job_recommendation import JobRecommendationController

from src.middleware.jwt_auth import jwt_auth

routes = Api(
    catch_all_404s=True,
    errors=errors,
    prefix='/api'
)

routes.add_resource(SignInController, '/auth/sign-in')
routes.add_resource(SignUpController, '/auth/sign-up')
routes.add_resource(SelfAuth, '/auth/self')

routes.add_resource(UserController, '/user')

routes.add_resource(JobRecommendationController, '/job-recommendation')