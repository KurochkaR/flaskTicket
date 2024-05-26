from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from app import db
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)


class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', backref='group', lazy=True)
    tickets = db.relationship('Ticket', backref='group', lazy=True)

    @staticmethod
    def get_choices():
        if current_user and not current_user.is_admin():
            groups = Group.query.filter_by(id=current_user.group_id).all()
        else:
            groups = Group.query.all()
        group_choices = [(group.id, group.name) for group in groups]
        return group_choices


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.role.name == "Admin"


class TicketStatus(Enum):
    IN_REVIEW = 'IN_REVIEW'
    PENDING = 'PENDING'
    CLOSED = 'CLOSED'


class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(PgEnum(TicketStatus), nullable=False, default=TicketStatus.IN_REVIEW)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
