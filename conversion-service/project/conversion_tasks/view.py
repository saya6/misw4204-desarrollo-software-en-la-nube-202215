from project import Resource, request
from project.users.models import User 
from project.conversion_engine.engine import ConversionEngine
from .model import ConversionTask
import uuid

class ConversionTaskResource(Resource):
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
        full_path = "/datastore/{}.{}".format(file_identificator,filename)
        file_to_upload.save(full_path)
        new_convertion_task = ConversionTask(filename, new_format, full_path).prepare()
        current_user = User.get_by_username("admin") # TODO: change me!
        current_user.add_new_task(new_convertion_task)
        converted_filename_parts = filename.split(".")[:-1]
        converted_filename = '.'.join(converted_filename_parts)
        converted_file_full_path = "/datastore/{}.{}.{}".format(file_identificator, converted_filename, new_format.lower())
        
        # just for testing purpose
        ce = ConversionEngine().build_source_file_path(
            full_path
        ).build_source_file_format(
            new_convertion_task.get_file_format()
        ).build_target_file_path(
            converted_file_full_path
        ).build_taget_file_format(
            new_convertion_task.get_new_format()
        )
        ce.build()
        if ce.convert():
            return {"id": current_user.conversion_tasks[-1].id}, 200
        return {"status":"Error", "response": "conversion issue"}, 422
        