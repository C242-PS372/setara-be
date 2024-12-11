from flask import request, jsonify
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from src.utils.db import db
from src.models import User
from src.utils.uuid import is_valid_uuid


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