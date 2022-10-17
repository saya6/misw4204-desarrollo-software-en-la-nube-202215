from project import Resource
from flask import send_file

class FileRetrieverResource(Resource):
    def get(self, filename):
        fullfilepath = "/datastore/{}".format(filename,)
        try:
            return send_file(fullfilepath, attachment_filename=filename) 
        except Exception as e:
            return {"error": str(e)}      
