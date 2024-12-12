import datetime
from flask import request, jsonify
from flask_restful import Resource
from src.utils.db import db
from src.models.job_listing import JobListing, JobListingStatus
from src.utils.uuid import is_valid_uuid


class JobListingController(Resource):
    def get(self):
        try:
            job_listing_id = request.args.get("id")

            if(not job_listing_id or not is_valid_uuid(job_listing_id)):
                raise AttributeError
            
            job_listing = JobListing.query.get(job_listing_id)

            if(not job_listing):
                return {'message': 'Job listing not found'}, 404

            return jsonify({
                    'id': job_listing.id,
                    'company_id': job_listing.company_id,
                    'job_type_id': job_listing.job_type_id,
                    'status': job_listing.status,
                    'description': job_listing.description,
                    'created_at': job_listing.created_at,
                    'modified_at': job_listing.modified_at
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
            

    def post(self):
        try:
            # Get request body
            body = request.get_json()
            company_id = body.get('company_id')
            job_type_id = body.get('job_type_id')
            description = body.get('description')

            if (not (company_id and job_type_id and description)):
                return {'message': 'Bad Request'}, 400
            
            new_job_listing = JobListing(
                company_id=company_id,
                job_type_id=job_type_id,
                status=JobListingStatus.OPEN,
                description=description
            )

            db.session.add(new_job_listing)
            db.session.commit()
            return {'message': 'Job listing created successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def patch(self):
        try:
             # Get request body
            body = request.get_json()
            job_listing_id = body.get('id')
            company_id = body.get('company_id')
            job_type_id = body.get('job_type_id')
            description = body.get('description')
            status = body.get('status')

            job_listing = JobListing.query.get(job_listing_id)

            if not job_listing:
                return {'message': 'Job listing not found'}, 404
        
            if(company_id):
                job_listing.company_id = company_id
            if(job_type_id):
                job_listing.job_type_id = job_type_id
            if(description):
                job_listing.description = description
            if(status):
                job_listing.status = status

            job_listing.modified_at = datetime.datetime.now()

            db.session.commit()
            return {'message': 'Job listing updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def delete(self):
        try:
             # Get request body
            body = request.get_json()
            job_listing_id = body.get('id')

            job_listing = JobListing.query.get(job_listing_id)

            if not job_listing:
                return {'message': 'Job listing not found'}, 404

            db.session.delete(job_listing)
            db.session.commit()
            return {'message': 'Job application deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500