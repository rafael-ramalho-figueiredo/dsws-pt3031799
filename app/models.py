from . import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class Email(db.Model):
    __tablename__ = 'emails'
    username = db.Column(db.String(64), primary_key=True)
    recipient = db.Column(db.String(64), index=True)
    subject = db.Column(db.String(64), index=True)
    text = db.Column(db.String(255), index=True)
    datetime_email = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Email %r>' % self.username