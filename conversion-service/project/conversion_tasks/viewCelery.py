from project import Resource, request
from project.users.models import User 
from .model import ConversionTask, ConversionTaskSchema
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
import project.task_daemon.celery_daemon as CDeamon

conversion_task_schema = ConversionTaskSchema();

class ConversionTaskCeleryResource(Resource):

    @jwt_required()
    def post(self):
        file_to_upload = request.files['file']
        filename = request.form.get('filename')
        if not ConversionTask.validate_file(filename):
            return {"status":"Error", "response": "bad file extension"}, 401
        new_format = request.form.get('new_format')
        if  not ConversionTask.validate_format(new_format):
            return {"status":"Error", "response": "bad formatting target"}, 401
        # Save the file into the disk
        file_identificator = uuid.uuid4()
        full_unique_filename = "{}.{}".format(file_identificator,filename)
        full_path = "/datastore/{}".format(full_unique_filename)
        
        file_to_upload.save(full_path)
        new_convertion_task = ConversionTask(filename, new_format, full_path).prepare()
        
        converted_filename_parts = filename.split(".")[:-1]
        converted_filename = '.'.join(converted_filename_parts)
        full_converted_unique_filename = "{}.{}.{}".format(file_identificator, converted_filename, new_format.lower())
        converted_file_full_path = "/datastore/{}".format(full_converted_unique_filename)
        new_convertion_task.set_file_converted_path(converted_file_full_path)
        user_from_jwt = get_jwt_identity()
        current_user = User.get_by_username(user_from_jwt)
        current_user.add_new_task(new_convertion_task)
        task = CDeamon.excecuteTask.delay(new_convertion_task.id)
        new_convertion_task.set_celery_task_id(task.id)        
        return {
            "id": new_convertion_task.id,
            "uploaded_unique_filename": full_unique_filename,
            "converted_unique_filename": full_converted_unique_filename,
            "celery_task_id": task.id
        }, 200
    
    @jwt_required()
    def get(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
          return {"status":"Error", "response": "This tasks owns to another user"}, 401 
        
        task = ConversionTask.get_tasks_by_id(id_task)
        response = conversion_task_schema.dump(task)
        return response

    @jwt_required()
    def put(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
           return {"status":"Error", "response": "This tasks owns to another user"}, 401 

        new_format = request.form.get('new_format')
        if  not ConversionTask.validate_format(new_format):
            return {"status":"Error", "response": "bad formatting target"}, 401
            
        convertion_task = ConversionTask.update_task(id_task, new_format)
        task = CDeamon.excecuteTask.delay(convertion_task.id)
        convertion_task.set_celery_task_id(task.id) 
        response = conversion_task_schema.dump(convertion_task)
        return response

    @jwt_required()
    def delete(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
           return {"status":"Error", "response": "This tasks owns to another user"}, 401 

        if not ConversionTask.validate_status_task(id_task):
            return {"status":"Error", "response": "Task is not in PROCESSED status"}, 401

        ConversionTask.delete_task(id_task)


def validate_task(id_task, user_from_jwt): 
    current_user = User.get_by_username(user_from_jwt)
    response = ConversionTask.validate_task_from_user(id_task, current_user.id)   
    
    return response
