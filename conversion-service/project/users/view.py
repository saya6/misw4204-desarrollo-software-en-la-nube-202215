from project import Resource, request
from .models import User
from flask_jwt_extended import JWTManager, create_access_token
import uuid
import re

class Constante:
    # Regular expression for validating an Email
    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' 

class SignInResource(Resource):
    def post(self):
        username=request.json['username']
        password1=request.json['password1']
        password2=request.json['password2']
        email=request.json['email']

        if(not re.fullmatch(Constante.EMAIL_REGEX, email)): 
            return "Email format is not correct", 401 

        if password1 != password2 :
            return "Passwords must be equals", 401

        foundUser = User.get_by_username(username) 

        if foundUser:
            return "User was already created in system", 401

        foundEmail = User.get_by_email(email) 
        
        if foundEmail:
            return "Email was already created in system", 401           

        User.create_user(User(username=username, password = password1, email = email))
        
        return {"status":"created"}, 200
