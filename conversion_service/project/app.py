from project import create_app, ext_celery, Api, db
from project.authentication.auth import AuthenticationResource
from project.users.view import SignInResource
from project.conversion_tasks.view import ConversionTaskResource, TaskResource
from project.file_retriever.view import FileRetrieverResource
from project.healthcheck.view import HealthcheckResource
from flask_jwt_extended import JWTManager

app = create_app()
api = Api(app)

api.add_resource(AuthenticationResource, '/api/auth/login')
api.add_resource(SignInResource, '/api/auth/signup')
api.add_resource(ConversionTaskResource, '/api/task','/api/task/<int:id_task>')
api.add_resource(TaskResource, '/api/tasks','/api/tasks/<int:order>', '/api/tasks/<int:order>/<int:max>')
api.add_resource(FileRetrieverResource, '/api/files/<string:filename>')
api.add_resource(HealthcheckResource, '/')

jwt = JWTManager(app)

