import datetime
from flask import request, jsonify
from flask_restful import Resource
from src.utils.db import db
from src.models.job_application import JobApplication
from src.utils.uuid import is_valid_uuid


class JobApplicationController(Resource):
    def get(self):
        try:
            job_application_id = request.args.get("id")

            if(not job_application_id or not is_valid_uuid(job_application_id)):
                raise AttributeError
            
            job_application = JobApplication.query.get(job_application_id)

            if(not job_application):
                return {'message': 'Job application not found'}, 404

            return jsonify({
                    'id': job_application.id,
                    'user_id': job_application.user_id,
                    'job_listing_id': job_application.job_listing_id,
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
            

    def post(self):
        try:
            # Get request body
            body = request.get_json()
            user_id = body.get('user_id')
            job_listing_id = body.get('job_listing_id')

            if (not (user_id and job_listing_id)):
                return {'message': 'Bad Request'}, 400
            
            new_job_application = JobApplication(
                user_id=user_id,
                job_listing_id=job_listing_id
            )

            db.session.add(new_job_application)
            db.session.commit()
            return {'message': 'job_application created successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def patch(self):
        try:
             # Get request body
            body = request.get_json()
            job_application_id = body.get('id')
            user_id = body.get('user_id')
            job_listing_id = body.get('job_listing_id')

            job_application = JobApplication.query.get(job_application_id)

            if not job_application:
                return {'message': 'Job application not found'}, 404
        
            if(user_id):
                job_application.user_id = user_id
            if(job_listing_id):
                job_application.job_listing_id = job_listing_id

            job_application.modified_at = datetime.datetime.now()

            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def delete(self):
        try:
             # Get request body
            body = request.get_json()
            job_application_id = body.get('id')

            job_application = JobApplication.query.get(job_application_id)

            if not job_application:
                return {'message': 'Job application not found'}, 404

            db.session.delete(job_application)
            db.session.commit()
            return {'message': 'Job application deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500