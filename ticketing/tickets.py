from datetime import date, datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.forms.customersearchform import CustomerSearchForm
from ticketing.forms.ticketform import TicketForm
from ticketing.forms.completeticketform import CompleteTicketForm
from ticketing.models import Ticket, Customer
from . import db

bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@bp.route('/')
def main():
    """Displays a grid of all tickets."""

    tickets = Ticket.query.order_by(Ticket.id).all()
    return render_template('app/ticket/tickets.html', tickets = tickets)


@bp.route('/landing', methods=('GET', 'POST'))
@login_required
def customer_landing():
    """View to either add an existing customer or create a new one."""

    if request.method == "POST":
        if request.form.get('create'):
            return redirect(url_for('tickets.new_customer'))

        if request.form.get('search'):
            searchform = CustomerSearchForm(request.form)
            customer = Customer.query.filter_by(lastname = searchform.lastname.data).first_or_404()
            

            return redirect(url_for('tickets.create', id = customer.id))

    return render_template('app/customer_landing.html')


@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    """View to create a new Ticket. Takes a Customer id as a parameter."""

    ticketform = TicketForm(request.form)

    if request.method == 'POST' and ticketform.validate():
        customer = Customer.query.filter_by(id = id).first_or_404()
        #TODO Customer Id should be checked to be valid.
        ticket = Ticket(customer.id, ticketform.tickettype.data, ticketform.ticketdescription.data,
            ticketform.ticketstatus.data, ticketform.promised.data, ticketform.notes.data)

        db.session.add(ticket)
        db.session.commit()        
        return redirect(url_for('tickets.main'))

    return render_template('app/ticket/create.html', id = id)


def get_ticket(id) -> Ticket:
    """Get a Ticket from the database and returns a 404 Error if not found."""

    ticket = Ticket.query.filter_by(id=id).first_or_404()
    return ticket


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """View to delete a Ticket."""

    ticket = get_ticket(id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('tickets.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """View to update a Ticket and store the changes."""

    ticket = get_ticket(id)
    updateform = TicketForm(request.form)

    if request.method == 'POST' and updateform.validate():
        ticket.tickettype = updateform.tickettype.data
        ticket.ticketdescription = updateform.ticketdescription.data
        ticket.ticketstatus = updateform.ticketstatus.data
        ticket.promised = updateform.promised.data

        db.session.commit()
        return redirect(url_for('tickets.main'))
    
    return render_template('app/ticket/update.html', ticket = ticket)


@bp.route('/<int:id>/complete', methods=('GET', 'POST'))
@login_required
def complete(id):
    """View to complete a ticket and set its status to done."""
    ticket = get_ticket(id)
    completeform = CompleteTicketForm(request.form)
    if request.method == 'POST' and completeform.validate():
        labor = completeform.labor.data
        parts = completeform.parts.data
        other = completeform.other.data
        notes = completeform.notes.data
        ticket.bDone = True
        ticket.bNotified = completeform.bNotified.data
        ticket.ticketstatus = 'completed'
        ticket.completed = datetime.now()

        db.session.commit()
        return redirect(url_for('tickets.main'))

    return render_template('app/ticket/complete.html', id = id, ticket = ticket)


@bp.route('/<int:id>/view')
@login_required
def view(id):
    """View to display a single Ticket object."""
    ticket = get_ticket(id)

    return render_template('app/ticket/view.html', ticket = ticket)

@bp.route('/options', methods=('GET', 'POST'))
@login_required
def options():


    return render_template('app/ticket/options')
