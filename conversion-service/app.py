
from project import create_app, ext_celery, Api, db
from project.authentication.auth import AuthenticationResource

app = create_app()
api = Api(app)
celery = ext_celery.celery

api.add_resource(AuthenticationResource, '/users/authenticate', resource_class_kwargs={'db': db})
