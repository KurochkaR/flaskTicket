from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app import db
from app.forms import TicketForm
from app.models import Group, Ticket, TicketStatus

ticket = Blueprint('ticket', __name__)


@ticket.route('/')
@login_required
def tickets_list():
    if current_user.is_admin():
        tickets = Ticket.query.order_by(Ticket.id).all()
    else:
        tickets = Ticket.query.filter_by(group_id=current_user.group_id).order_by(Ticket.id).all()
    return render_template('tickets.html', title='Tickets', tickets=tickets)


@ticket.route('/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    action_url = url_for('ticket.new_ticket')
    button = "Create"
    form = TicketForm()
    group_choices = Group.get_choices()
    if len(group_choices) == 1:
        form.group.choices = group_choices
        form.group.data = str(group_choices[0][0])
        form.group.render_kw = {'disabled': 'disabled'}
    else:
        form.group.choices = group_choices

    if form.validate_on_submit():
        ticket_create = Ticket(title=form.title.data,
                               description=form.description.data,
                               status=form.status.data,
                               group_id=form.group.data)
        db.session.add(ticket_create)
        db.session.commit()
        flash('Ticket has been created!', 'success')
        return redirect(url_for('ticket.tickets_list'))
    return render_template('create_ticket.html', title='New Ticket', form=form, action=action_url, button=button)


@ticket.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    action_url = url_for('ticket.edit_ticket', ticket_id=ticket_id)
    button = "Edit"
    upd_ticket = Ticket.query.get(ticket_id)
    form = TicketForm(obj=upd_ticket)
    group_choices = Group.get_choices()
    if len(group_choices) == 1:
        form.group.choices = group_choices
        form.group.data = str(group_choices[0][0])
        form.group.render_kw = {'disabled': 'disabled'}
    else:
        form.group.choices = group_choices
    if request.method == 'GET':
        form.status.data = upd_ticket.status.name
    if form.validate_on_submit():
        upd_ticket.title = form.title.data
        upd_ticket.description = form.description.data
        upd_ticket.group_id = form.group.data
        upd_ticket.status = form.status.data
        db.session.commit()
        flash('Ticket has been updated!', 'success')
        return redirect(url_for('ticket.tickets_list'))
    return render_template('create_ticket.html', title='Edit Ticket', form=form, action=action_url, button=button)


@ticket.route('/delete/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def delete(ticket_id):
    del_ticket = Ticket.query.get(ticket_id)
    if not del_ticket:
        flash('Ticket not found!', 'error')
        return redirect(url_for('ticket.tickets_list'))
    db.session.delete(del_ticket)
    db.session.commit()
    flash('Ticket has been deleted!', 'success')
    return redirect(url_for('ticket.tickets_list'))
