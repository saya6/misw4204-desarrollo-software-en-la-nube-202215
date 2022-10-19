# from celery import current_app as current_celery_app

# def make_celery(app):
#     celery = current_celery_app
#     celery.config_from_object(app.config, namespace="CELERY")

#     return celery

from celery import Celery 
from flask import Flask
 
def init_celery(celery: Celery, app: Flask): 
    celery.conf.update(app.config) 
    TaskBase = celery.Task 
    class ContextTask(TaskBase): 
        def __call__(self, *args, **kwargs): 
            with app.app_context(): 
                return TaskBase.__call__(self, *args, **kwargs) 
    celery.Task = ContextTask 
