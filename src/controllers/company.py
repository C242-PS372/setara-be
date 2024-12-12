import datetime
from flask import request, jsonify
from flask_restful import Resource
from src.utils.db import db
from src.models.company import Company
from src.utils.uuid import is_valid_uuid


class CompanyController(Resource):
    def get(self):
        try:
            company_id = request.args.get("id")

            if(not company_id or not is_valid_uuid(company_id)):
                raise AttributeError
            
            company = Company.query.get(company_id)

            if(not company):
                return {'message': 'Company not found'}, 404

            return jsonify({
                    'id': company.id,
                    'name': company.name,
                    'decription': company.decription,
                    'created_at': company.created_at
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
            

    def post(self):
        try:
            # Get request body
            body = request.get_json()
            name = body.get('name')
            description = body.get('description')

            if (not (body and name)):
                return {'message': 'Bad Request'}, 400
            
            new_company = Company(
                name=name,
                description=description
            )

            db.session.add(new_company)
            db.session.commit()
            return {'message': 'Company created successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def patch(self):
        try:
             # Get request body
            body = request.get_json()
            company_id = body.get('id')
            description = body.get('description')

            company = Company.query.get(company_id)

            if not company:
                return {'message': 'Company not found'}, 404
        
            if(description):
                company.description = description

            company.modified_at = datetime.datetime.now()

            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def delete(self):
        try:
             # Get request body
            body = request.get_json()
            company_id = body.get('id')

            company = Company.query.get(company_id)

            if not company:
                return {'message': 'Company not found'}, 404

            db.session.delete(company)
            db.session.commit()
            return {'message': 'Company deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500