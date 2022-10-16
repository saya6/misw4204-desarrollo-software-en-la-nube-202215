from pickle import FALSE
from project import db
from sqlalchemy import DateTime
import datetime
import enum

class ConversionTaskStatus(enum.Enum):
    UPLOADED = "UPLOADED"
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
    db.relationship("User", back_populates="conversion_tasks")

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

    def get_file_format(self):
        return self.file_format

    def get_new_format(self):
        return self.file_new_format

    def get_file_converted_path(self):
        return self.file_converted_path

    @staticmethod
    def validate_format(file_new_format):
        return file_new_format.upper() in ConversionTaskFormats._value2member_map_

    @staticmethod
    def validate_file(filename):
        file_parts = filename.split(".")
        return ConversionTask.validate_format(file_parts[-1])
