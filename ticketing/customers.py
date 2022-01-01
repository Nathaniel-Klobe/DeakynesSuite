from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from ticketing.auth import login_required
from ticketing.forms.customerform import CustomerForm
from ticketing.models import Customer, Ticket
from . import db

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/')
def main():
    """Displays a grid of all customers."""

    customers = Customer.query.order_by(Customer.id).all()
    return render_template('app/customer/customers.html', cust = customers)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new customer."""

    customerform = CustomerForm(request.form)
    if request.method == 'POST' and customerform.validate():
        customer = Customer(customerform.firstname.data, customerform.lastname.data,
            customerform.address.data, customerform.phone.data, customerform.email.data)

        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('customers.main'))

    return render_template('app/customer/create.html')


def get_customer(id):
    """Get a Customer from the database and returns a 404 Error if not found."""

    customer = Customer.query.filter_by(id=id).first_or_404()
    return customer


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Delete the customer from the database"""

    customer = get_customer(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a current customer. Takes an id as a parameter."""

    customer = get_customer(id)
    customerform = CustomerForm(request.form)
    if request.method == 'POST' and customerform.validate():
        customer.firstname = customerform.firstname.data
        customer.lastname = customerform.lastname.data
        customer.address = customerform.address.data
        customer.phone = customerform.phone.data
        customer.email = customerform.email.data

        db.session.commit()

        return redirect(url_for('customer.main'))
    
    return render_template('app/ticket/update.html', customer = customer)


@bp.route('/<int:id>/view')
@login_required
def view(id):
    """View a Customer. Takes an id as a parameter."""
    
    customer = get_customer(id)
    tickets = Ticket.query.filter_by(customer_id = id).order_by(Ticket.id).all()

    return render_template('app/customer/view.html', customer = customer, tickets = tickets)


@bp.route('/options', methods=('GET', 'POST'))
@login_required
def options():
    

    return render_template('app/customer/options')
