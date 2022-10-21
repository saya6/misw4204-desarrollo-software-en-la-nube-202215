import os

from flask import Flask, request
from flask_restful import Api, Resource
from flask_celeryext import FlaskCeleryExt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from celery import Celery
from project.celery_utils import init_celery

from project.config import config


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
#ext_celery = FlaskCeleryExt(create_celery_app=make_celery)


def make_celery(app_name = __name__):
    redis_uri = "redis://localhost:6379"
    return Celery(app_name, backend=redis_uri, broker=redis_uri)

celery = make_celery()

def create_app(**kwargs):
    if "config_name" in kwargs:
        config_name = kwargs["config_name"]
    else:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    # instantiate the app
    app = Flask(__name__)

    # set config
    app.config.from_object(config[config_name])

    if "celery" in kwargs:
        init_celery(kwargs["celery"], app)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    #ext_celery.init_app(app)

    # add auth
    JWTManager(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app