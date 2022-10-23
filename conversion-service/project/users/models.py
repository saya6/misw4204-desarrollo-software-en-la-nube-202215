from project import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    conversion_tasks = db.relationship('ConversionTask', cascade='all, delete, delete-orphan')

    def __init__(self, username, email, password, *args, **kwargs):
        self.username = username
        self.email = email
        self.password = password

    def add_new_task(self, task):
        self.conversion_tasks.append(task)
        db.session.commit()
    
    def check_auth(self, password):
        if self.password == password:
            return True
        return False

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()
        return user
