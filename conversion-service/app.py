from project import create_app, Api, db
from project.authentication.auth import AuthenticationResource
from project.users.view import SignInResource
from project.conversion_tasks.view import ConversionTaskResource, TaskResource
from project.file_retriever.view import FileRetrieverResource
from project.conversion_tasks.viewCelery import ConversionTaskCeleryResource
from flask_jwt_extended import JWTManager
from project import celery

app = create_app(celery=celery)
api = Api(app)
#celery = ext_celery.celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])

api.add_resource(AuthenticationResource, '/api/auth/login')
api.add_resource(SignInResource, '/api/auth/signup')
api.add_resource(ConversionTaskResource, '/api/task','/api/task/<int:id_task>')
api.add_resource(TaskResource, '/api/tasks','/api/tasks/<int:order>', '/api/tasks/<int:order>/<int:max>')
api.add_resource(FileRetrieverResource, '/api/files/<string:filename>')

api.add_resource(ConversionTaskCeleryResource, '/api/taskCelery', '/api/taskCelery/<id_task>')

jwt = JWTManager(app)

