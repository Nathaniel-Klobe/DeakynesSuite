from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.database import get_db

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/')
def main():
    db = get_db()
    cust = db.execute(
        'SELECT * FROM customer'
    ).fetchall()
    return render_template('app/customer/customers.html', cust = cust)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        first_name = request.form['first_name'].lower()
        last_name = request.form['last_name'].lower()
        street_address = request.form['street_address'].lower()
        phone = request.form['phone']
        
        error = None

        if not first_name:
            error = 'First Name Required.'
        elif not last_name:
            error = 'Last Name Required.'
        elif not street_address:
            error = 'Address Required.'
        elif not phone:
            error = 'Phone Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO customer (first_name, last_name, street_address, phone) VALUES(?, ?, ?, ?)',
                (first_name, last_name, street_address, phone)
            )
            db.commit()
            return redirect(url_for('customers.main'))
    return render_template('app/customer/create.html')


def get_customer(id):
    customer = get_db().execute(
        'SELECT id, first_name, last_name, street_address, phone'
        ' FROM customer'
        ' WHERE id = ?', (id,)
    ).fetchone()

    if customer is None:
        abort(404, f"Customer id {id} doesn't exist.")

    return customer


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_customer(id)
    db = get_db()
    db.execute('DELETE FROM customer WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('customers.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    customer = get_customer(id)

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['ticket_description']
        street_address = request.form.get('street_address')
        phone = request.form['promised']
        error = None

        if not first_name:
            error = 'First Name Required.'
        elif not last_name:
            error = 'Last Name Required.'
        elif not phone:
            error = 'Phone Required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE customer SET first_name = ?, last_name = ?, street_address = ?, phone = ?'
                ' WHERE id = ?',
                (first_name, last_name, street_address, phone, id)
            )
            db.commit()
            return redirect(url_for('customer.main'))
    
    return render_template('app/ticket/update.html', customer = customer)


@bp.route('/<int:id>/view')
@login_required
def view(id):
    customer = get_customer(id)

    db = get_db()
    tickets = db.execute(
        'SELECT t.id, ticket_type, ticketstatus, reference, created'
        ' FROM ticket t JOIN customer c ON t.customer_id = c.id'
        ' WHERE customer_id = ?'
        ' ORDER BY created DESC',
        (id,)
    ).fetchall()
    orders = db.execute(
        'SELECT o.id, order_type, created'
        ' FROM specialorder o JOIN customer c ON o.customer_id = c.id'
        ' WHERE customer_id = ?'
        ' ORDER BY created DESC',
        (id,)
    ).fetchall()
    rentals = db.execute(
        'SELECT r.id, rentalitem, created, promised'
        ' FROM rental r JOIN customer c ON r.customer_id = c.id'
        ' WHERE customer_id = ?'
        ' ORDER BY created DESC',
        (id,)
    ).fetchall()

    return render_template('app/customer/view.html', customer = customer, tickets = tickets, orders = orders, rentals = rentals)


@bp.route('/options', methods=('GET', 'POST'))
@login_required
def options():
    

    return render_template('app/customer/options')
