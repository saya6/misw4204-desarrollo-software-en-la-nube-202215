from project import Resource, request
from project.users.models import User
from flask_jwt_extended import JWTManager, create_access_token

class AuthenticationResource(Resource):
    def post(self):
        username=request.json['username']
        password=request.json['password']
        user = User.get_by_username(username)
        if  user is not None:
            if user.check_auth(password):
                jwt = create_access_token(identity=username)
                return {"status":"authenticated", "JWT": jwt}, 200
        return {"status":"Error", "response": "bad credentials"}, 401