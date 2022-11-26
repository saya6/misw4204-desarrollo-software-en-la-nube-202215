# from celery import current_app as current_celery_app

# def make_celery(app):
#     celery = current_celery_app
#     celery.config_from_object(app.config, namespace="CELERY")

#     return celery

from celery import Celery 
 
def make_celery(app): 
    celery = Celery( 
        app.import_name, broker=app.config['CELERY_BROKER_URL'], include=["project.task_daemon"]
    ) 
    celery.conf.update(app.config) 
    TaskBase = celery.Task 
    class ContextTask(TaskBase): 
        abstract = True 
        def __call__(self, *args, **kwargs): 
            with app.app_context(): 
                return TaskBase.__call__(self, *args, **kwargs) 
    celery.Task = ContextTask 
    return celery 