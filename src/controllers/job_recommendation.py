import datetime
from flask import request, jsonify
from flask_restful import Resource
from src.utils.db import db
from src.utils.predict_model import PredictModel
from src.models.user import User
from src.models.job_recommendation import JobRecommendation
from src.models.job_type import JobType
from src.utils.uuid import is_valid_uuid


class JobRecommendationController(Resource):
    def get(self):
        try:
            job_recommendtaion_id = request.args.get("id")

            if(not job_recommendtaion_id or not is_valid_uuid(job_recommendtaion_id)):
                raise AttributeError
            
            job_recommendation = JobRecommendation.query.get(job_recommendtaion_id)

            if(not job_recommendation):
                return {'message': 'Job reccomendation not found'}, 404

            return jsonify({
                    'id': job_recommendation.id,
                    'user_id': job_recommendation.user_id,
                    'job_type_id': job_recommendation.job_typjob_type_ide_id,
                    'created_at': job_recommendation.created_at,
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
            

    def post(self):
        try:
            # Get request body
            body = request.get_json()
            disability = body.get('disability')
            age = body.get('age')
            experience = body.get('experience')
            city = body.get('city')
            user_id = body.get('user_id')

            if (not (disability and age and experience and city and user_id)):
                return {'message': 'Bad Request'}, 400
            
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            
            user.age = age
            user.disability = disability
            user.city = city
            user.experience = experience

            job_recommendation = PredictModel().predict(
                disability=disability,
                age=age,
                experience=experience,
                city=city
            )

            job_type = JobType.query.filter_by(title=job_recommendation).first()

            if(job_type):
                new_job_recommendation = JobRecommendation(
                    user_id = user_id,
                    job_type_id = job_type.id
                )
                db.session.add(new_job_recommendation)
            else :
                new_job_type = JobType(
                    title = job_recommendation
                )
                db.session.add(new_job_type)
                db.session.commit()

                new_job_recommendation = JobRecommendation(
                    user_id = user_id,
                    job_type_id = new_job_type.id
                )
                db.session.add(new_job_recommendation)

            db.session.commit()
            return {'message': job_recommendation}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500