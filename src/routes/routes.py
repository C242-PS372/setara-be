from flask_restful import Api
from src.utils.errors import errors
from src.controllers.user import UserController, UserAllController, UserJobRecommendationController
from src.controllers.auth import SignInController, SignUpController, SelfAuth
from src.controllers.job_recommendation import JobRecommendationController, JobRecommendationAlternateController
from src.controllers.company import CompanyController
from src.controllers.job_application import JobApplicationController
from src.controllers.job_listing import JobListingController

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
routes.add_resource(UserAllController, '/user/all')
routes.add_resource(UserJobRecommendationController, '/user/recommendation')


routes.add_resource(CompanyController, '/job-listing')

routes.add_resource(JobRecommendationController, '/job-recommendation')
routes.add_resource(JobRecommendationAlternateController, '/job-recommendation-inference')
routes.add_resource(JobApplicationController, '/job-application')
routes.add_resource(JobListingController, '/job-listing')