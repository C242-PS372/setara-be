from flask import request, jsonify
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from sqlalchemy import or_, select
from src.utils.db import db
from src.models.user import User
from src.models.job_recommendation import JobRecommendation
from src.models.job_type import JobType
from src.utils.uuid import is_valid_uuid
from src.utils.parse_int import parse_int


class UserController(Resource):
    def get(self):
        try:
            user_id = request.args.get("id")

            if(not user_id or not is_valid_uuid(user_id)):
                raise AttributeError
            
            user = User.query.get(user_id)

            if(not user):
                return {'message': 'User not found'}, 404

            return jsonify({
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
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
            username = body.get('username')
            password = body.get('password')
            email = body.get('email')

            if (not (body and name and username and password)):
                return {'message': 'Bad Request'}, 400
            
            salt = gensalt()
            hashed_password = hashpw(password.encode('utf-8'), salt)

            new_user = User(
                name=name,
                username=username,
                password=hashed_password.decode('utf-8'),
                email=email
            )
        
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def patch(self):
        try:
             # Get request body
            body = request.get_json()
            user_id = body.get('id')
            name = body.get('name')
            username = body.get('username')
            password = body.get('password')
            email = body.get('email')

            user = User.query.get(user_id)

            if not user:
                return {'message': 'User not found'}, 404
        
            if(name):
                user.name = name
            if(username):
                user.username = username
            if(email):
                user.email = email
            if (password):
                salt = gensalt()
                hashed_password = str(hashpw(password.encode('utf-8'), salt))
                user.password = hashed_password

            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500

    def delete(self):
        try:
             # Get request body
            body = request.get_json()
            user_id = body.get('id')

            user = User.query.get(user_id)

            if not user:
                return {'message': 'User not found'}, 404

            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error occurred: {str(e)}'}, 500
        
class UserAllController(Resource):
    def get(self):
        try:
            search = request.args.get("search", "")
            page = parse_int(request.args.get("page"), 1)
            limit = parse_int(request.args.get("limit"), 10)

            page = 1
            limit = 10
            
            if page < 1:
                page = 1
            if limit < 1:
                limit = 10

            query = User.query
            if search:
                query = query.filter(
                    or_(
                        User.name.like(f"%{search}%"),
                        User.username.like(f"%{search}%"),
                        User.email.like(f"%{search}%")
                    )
                )
            
            offset = (page - 1) * limit
            users = query.offset(offset).limit(limit).all()

            return jsonify({
                "users": users,
                "page": page,
                "limit": limit,
                "total": query.count()
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

class UserJobRecommendationController(Resource):
    def get(self):
        try:
            user_id = request.args.get("user_id")

            query = (
                select(JobType.title)
                .select_from(JobRecommendation)
                .join(JobType, JobRecommendation.job_type_id == JobType.id)
                .where(JobRecommendation.user_id == user_id)
                .order_by(JobRecommendation.created_at.desc())
            )
            results = db.session.execute(query).scalars().all()

            return jsonify({
                "job_recommendation": results[0],
                "job_recommendation_all": results,
            })
        
        except AttributeError :
            return {"message" : "Bad Request"}, 400
        
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

            