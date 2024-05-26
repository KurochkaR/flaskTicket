from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import Role, Group, User

auth = Blueprint('auth', __name__)


@auth.route("/")
def index():
    return redirect(url_for('ticket.tickets_list'))


@auth.route("/register", methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('ticket.tickets_list'))
    role_choices = [(role.id, role.name) for role in Role.query.all()]
    group_choices = [(group.id, group.name) for group in Group.query.all()]
    form = RegistrationForm()
    form.role.choices = role_choices
    form.group.choices = group_choices
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    role_id=form.role.data,
                    group_id=form.group.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('ticket.tickets_list'))
    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ticket.tickets_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('ticket.tickets_list'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
