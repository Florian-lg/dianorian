"""Import some useful modules"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    """User class"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    firstname = db.Column(db.String(120), index=True, unique=False)
    lastname = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """Password setter"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Define user"""
        return '<User {}>'.format(self.username)

class Tweet(db.Model):
    """Tweet class"""
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tweet {}>'.format(self.body)

@login.user_loader
def load_user(user_id):
    """Used to load user"""
    return User.query.get(int(user_id))
