import datetime
from flask import request, jsonify
from flask_restful import Resource
from src.utils.db import db
from src.utils.predict_model import PredictModel
from src.models.job_recommendation import JobRecommendation
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
            
            job_recommendation = PredictModel._instance.predict(
                disability=disability,
                age=age,
                experience=experience,
                city=city)
            
            # new_job_recommendation = JobRecommendation(
            #     company_id=company_id,
            #     job_type_id=job_type_id,
            #     status=JobRecommendationStatus.OPEN,
            #     description=description
            # )

            # db.session.add(new_job_recommendation)
            # db.session.commit()
            return {'message': job_recommendation}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    # def patch(self):
    #     try:
    #          # Get request body
    #         body = request.get_json()
    #         job_recommendtaion_id = body.get('id')
    #         company_id = body.get('company_id')
    #         job_type_id = body.get('job_type_id')
    #         description = body.get('description')
    #         status = body.get('status')

    #         job_recommendation = JobRecommendation.query.get(job_recommendtaion_id)

    #         if not job_recommendation:
    #             return {'message': 'Job listing not found'}, 404
        
    #         if(company_id):
    #             job_recommendation.company_id = company_id
    #         if(job_type_id):
    #             job_recommendation.job_type_id = job_type_id
    #         if(description):
    #             job_recommendation.description = description
    #         if(status):
    #             job_recommendation.status = status

    #         job_recommendation.modified_at = datetime.datetime.now()

    #         db.session.commit()
    #         return {'message': 'Job listing updated successfully'}, 200
    #     except Exception as e:
    #         db.session.rollback()
    #         return {'message': f'Error occurred: {str(e)}'}, 500

    # def delete(self):
    #     try:
    #          # Get request body
    #         body = request.get_json()
    #         job_recommendtaion_id = body.get('id')

    #         job_recommendation = JobRecommendation.query.get(job_recommendtaion_id)

    #         if not job_recommendation:
    #             return {'message': 'Job listing not found'}, 404

    #         db.session.delete(job_recommendation)
    #         db.session.commit()
    #         return {'message': 'Job application deleted successfully'}, 200
    #     except Exception as e:
    #         db.session.rollback()
    #         return {'message': f'Error occurred: {str(e)}'}, 500