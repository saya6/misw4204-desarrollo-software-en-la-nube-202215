from urllib import response
from project import Resource, request
from project.users.models import User 
from .model import ConversionTask, ConversionTaskSchema
from project.file_store.file_store import FileStorage
from google.cloud import pubsub_v1
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
import json 


conversion_task_schema = ConversionTaskSchema();

class ConversionTaskResource(Resource):

    @jwt_required()
    def post(self):
        file_to_upload = request.files['file']
        filename = request.form.get('filename')
        if not ConversionTask.validate_file(filename):
            return {"status":"Error", "response": "bad file extension"}, 401
        new_format = request.form.get('new_format')
        if  not ConversionTask.validate_format(new_format):
            return {"status":"Error", "response": "bad formatting target"}, 401
        # Save the file into the bucket
        file_identificator = uuid.uuid4()
        full_unique_filename = "{}.{}".format(file_identificator,filename)
        file_store = FileStorage("miso_bfac_bucket")
        file_store.save_file(full_unique_filename,file_to_upload.read())
        new_convertion_task = ConversionTask(filename, new_format, full_unique_filename).prepare()
        converted_filename_parts = filename.split(".")[:-1]
        converted_filename = '.'.join(converted_filename_parts)
        full_converted_unique_filename = "{}.{}.{}".format(file_identificator, converted_filename, new_format.lower())
        new_convertion_task.set_file_converted_path(full_converted_unique_filename)

        user_from_jwt = get_jwt_identity()
        current_user = User.get_by_username(user_from_jwt)
        current_user.add_new_task(new_convertion_task)
        # enqueue the new conversion task
        publisher = pubsub_v1.PublisherClient()
        topic_path = "projects/bfac-366702/topics/conversion_tasks"
        response = {
            "id": current_user.conversion_tasks[-1].id,
            "uploaded_unique_filename": full_unique_filename,
            "converted_unique_filename": full_converted_unique_filename
        }
        task_message = "{}".format(response["id"]).encode('utf-8')
        future_response = publisher.publish(topic_path, task_message)
        response["queue_id"] = future_response.result()
        return response, 200
    
    @jwt_required()
    def get(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
           return {"status":"Error", "response": "This task owns to another user"}, 401 

        task = ConversionTask.get_tasks_by_id(id_task)
        response = conversion_task_schema.dump(task)
        return response

    @jwt_required()
    def put(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
           return {"status":"Error", "response": "This task owns to another user"}, 401 

        new_format = request.form.get('new_format')
        if  not ConversionTask.validate_format(new_format):
            return {"status":"Error", "response": "bad formatting target"}, 401

        if not ConversionTask.validate_status_task(id_task):
            return {"status":"Error", "response": "Task is not in PROCESSED status"}, 401
        
        task = ConversionTask.update_task(id_task, new_format)
        response = conversion_task_schema.dump(task)
        return response

    @jwt_required()
    def delete(self, id_task):
        if not validate_task(id_task, get_jwt_identity()):
           return {"status":"Error", "response": "This task owns to another user"}, 401 

        if not ConversionTask.validate_status_task(id_task):
            return {"status":"Error", "response": "Task is not in PROCESSED status"}, 401

        ConversionTask.delete_task(id_task)
        return "", 204

def validate_task(id_task, user_from_jwt): 
    current_user = User.get_by_username(user_from_jwt)
    response = ConversionTask.validate_task_from_user(id_task, current_user.id)   
    
    return response
        

class TaskResource(Resource):

    @jwt_required()    
    def get(self, order = 0, max=None):
        user_from_jwt = get_jwt_identity()
        logging.warning(user_from_jwt)
        current_user = User.get_by_username(user_from_jwt)
        tasks = ConversionTask.get_tasks(current_user.id, order, max)
        response = [conversion_task_schema.dump(task) for task in tasks]
        
        return response