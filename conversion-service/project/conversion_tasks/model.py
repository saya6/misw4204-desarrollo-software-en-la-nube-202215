from project import db
from sqlalchemy import DateTime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow_enum import EnumField
import datetime
import enum

class ConversionTaskStatus(enum.Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"

class ConversionTaskFormats(enum.Enum):
    MP3 = "MP3"
    WAV = "WAV"
    OGG = "OGG"


class ConversionTask(db.Model):

    __tablename__ = "conversion_tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(128), nullable=False)
    file_format = db.Column(db.Enum(ConversionTaskFormats), nullable=False)
    file_new_format = db.Column(db.Enum(ConversionTaskFormats), nullable=False)
    file_source_path = db.Column(db.String(250), nullable=False)
    file_converted_path = db.Column(db.String(250), nullable=False)
    task_status = db.Column(db.Enum(ConversionTaskStatus), nullable=False)
    timeStamp = db.Column(DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="conversion_tasks")

    def __init__(self, filename, file_new_format, file_source_path, *args, **kwargs):
        self.filename = filename
        self.file_new_format = ConversionTaskFormats[file_new_format.upper()]
        self.file_source_path = file_source_path
        self.task_status = ConversionTaskStatus.UPLOADED
    
    def prepare(self):
        file_parts = self.filename.split(".")
        self.file_format = ConversionTaskFormats[file_parts[-1].upper()]
        self.file_converted_path = ""
        return self

    def set_file_converted_path(self, new_path):
        self.file_converted_path = new_path

    def get_file_source_path(self):
        return self.file_source_path

    def get_file_format(self):
        return self.file_format

    def get_file_converted_path(self):
        return self.file_converted_path

    def get_new_format(self):
        return self.file_new_format

    def update_status_to_processing(self):
        self.task_status = ConversionTaskStatus.PROCESSING
        db.session.commit()

    def update_status_to_processed(self):
        self.task_status = ConversionTaskStatus.PROCESSED
        db.session.commit()

    @staticmethod
    def validate_format(file_new_format):
        return file_new_format.upper() in ConversionTaskFormats._value2member_map_

    @staticmethod
    def validate_file(filename):
        file_parts = filename.split(".")
        return ConversionTask.validate_format(file_parts[-1])
    
    @staticmethod
    def get_tasks(id_user, order, max):

        order_by = ConversionTask.id.asc()
        if order > 0:
            order_by = ConversionTask.id.desc()

        sentence = ConversionTask.query.filter_by(id = id_user).order_by(order_by)

        if max:
            sentence = ConversionTask.query.filter_by(id = id_user).order_by(order_by).limit(max)

        return sentence.all()

    @staticmethod
    def get_unprocessed_tasks():
        return ConversionTask.query.filter_by(task_status=ConversionTaskStatus.UPLOADED)
    
    @staticmethod
    def get_tasks_by_id(id):
        return ConversionTask.query.filter_by(id=id).first()

    @staticmethod
    def update_task(id, new_format):
        task = ConversionTask.query.get_or_404(id)
        task.task_status = ConversionTaskStatus.UPLOADED
        task.file_new_format = new_format

        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(id):

        task = ConversionTask.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def validate_task_from_user(id_task, id_user):
        return ConversionTask.query.filter_by(id = id_task).filter_by(id_user = id_user).first()    

    @staticmethod
    def validate_status_task(id_task):
        task = ConversionTask.get_tasks_by_id(id_task)    
        return task.task_status == ConversionTaskStatus.PROCESSED


class ConversionTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ConversionTask
        include_relationships = True
        load_instance = True

    file_format = EnumField(ConversionTaskFormats)
    file_new_format = EnumField(ConversionTaskFormats)
    task_status = EnumField(ConversionTaskStatus)
    timeStamp = fields.DateTime()
