from project import Resource
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.users.models import User 
from project.conversion_tasks.model import ConversionTask

class FileRetrieverResource(Resource):
    @jwt_required()
    def get(self, filename):
        fullfilepath = "/datastore/{}".format(filename,)
        if not validate_file(fullfilepath, get_jwt_identity()):
            return {"status":"Error", "response": "This file owns to another user or does not exist"}, 401 
        try:
            return send_file(fullfilepath, attachment_filename=filename) 
        except Exception as e:
            return {"error": str(e)}      

def validate_file(fullfilepath, user_from_jwt): 
    current_user = User.get_by_username(user_from_jwt)
    response = ConversionTask.validate_file_from_user(fullfilepath, current_user.id)   
    
    return response