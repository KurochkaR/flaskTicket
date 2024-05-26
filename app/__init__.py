
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    from .models import User, Role, Group, Ticket, TicketStatus

    db.init_app(app)
    db.Model = Base
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():

        from .views import auth, ticket
        app.register_blueprint(ticket.ticket, url_prefix="/tickets")
        app.register_blueprint(auth.auth)
        db.create_all()

        for role_name in ['Admin', 'Manager', 'Analyst']:
            if not Role.query.filter_by(name=role_name).first():
                db.session.add(Role(name=role_name))

        for group_name in ['Customer 1', 'Customer 2', 'Customer 3']:
            if not Group.query.filter_by(name=group_name).first():
                db.session.add(Group(name=group_name))
        db.session.commit()

    return app
