from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CallRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_type = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('call_request.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    confirmed_slot = db.Column(db.String(100), nullable=True)
