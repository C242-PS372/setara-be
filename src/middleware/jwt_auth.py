from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask_jwt_extended import jwt_required

def jwt_auth(fn):
    @wraps(fn)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            # forward
            return fn(*args, **kwargs)

        except ExpiredSignatureError:
            return {"message": "Token has expired."}, 401
        except InvalidTokenError:
            return {"message": "Invalid token."}, 401
        except Exception as e:
            return {"message": str(e)}, 500
    return decorated