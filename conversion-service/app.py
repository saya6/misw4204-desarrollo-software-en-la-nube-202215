from project import create_app, ext_celery, Api, db
from project.authentication.auth import AuthenticationResource
from project.users.view import SignInResource
from project.conversion_tasks.view import ConversionTaskResource
from project.file_retriever.view import FileRetrieverResource

app = create_app()
api = Api(app)
celery = ext_celery.celery

api.add_resource(AuthenticationResource, '/users/authenticate')
api.add_resource(SignInResource, '/users/signin')
api.add_resource(ConversionTaskResource, '/api/task')
api.add_resource(ConversionTaskResource, '/api/tasks','/api/tasks/<int:order>', '/api/tasks/<int:order>/<int:max>')
api.add_resource(FileRetrieverResource, '/api/files/<string:filename>')

