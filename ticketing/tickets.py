from datetime import date, datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.db import get_db

bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@bp.route('/')
def main():
    db = get_db()
    tickets = db.execute(
        'SELECT t.id, c.last_name, c.phone, ticket_type, ticket_description, created, promised'
        ' FROM ticket t JOIN customer c ON t.customer_id = c.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('app/ticket/tickets.html', tickets = tickets)


@bp.route('/landing', methods=('GET', 'POST'))
@login_required
def customer_landing():
    if request.method == "POST":
        if request.form.get('create'):
            return redirect(url_for('tickets.new_customer'))

        if request.form.get('search'):
            db = get_db()
            error = None
            last_name = request.form.get('last_name', False)
            customer = db.execute(
                'SELECT * FROM customer WHERE last_name = ?', (last_name,)
            ).fetchone()
        
            if not customer:
                error = 'No Customer Found.'

            if error is not None:
                flash(error)
            else:
                return redirect(url_for('tickets.create', id = customer['id']))

    return render_template('app/customer_landing.html')


@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    if request.method == 'POST':
        ticket_type = request.form['ticket_type']
        ticket_description = request.form['ticket_description']
        reference = request.form['reference']
        promised = request.form['promised']
        created = date.today()
        ticketstatus = 'New'
        customer_id = id
        error = None

        if not ticket_type:
            error = 'Ticket Type Required.'
        elif not ticket_description:
            error = 'Ticket Description Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO ticket (customer_id, ticket_type, ticket_description, reference, ticketstatus, created, promised) VALUES(?, ?, ?, ?, ?, ?, ?)',
                (customer_id, ticket_type, ticket_description, reference, ticketstatus, created, promised) 
            )
            db.commit()
            return redirect(url_for('tickets.main'))

    return render_template('app/ticket/create.html', id = id)

    
@bp.route('/create_customer', methods=('GET', 'POST'))
@login_required
def create_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        street_address = request.form['street_address']
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
            result = db.execute(
                'INSERT INTO customer (first_name, last_name, street_address, phone) VALUES(?, ?, ?, ?)',
                (first_name, last_name, street_address, phone)
            )
            db.commit()
            customer_id = result.lastrowid
            return redirect(url_for('tickets.create', id = customer_id))
    return render_template('app/customer/create.html')


def get_ticket(id):
    ticket = get_db().execute(
        'SELECT t.id, c.last_name, c.phone, ticket_type, ticket_description, created, promised'
        ' FROM ticket t JOIN customer c ON t.customer_id = c.id'
        ' WHERE t.id = ?', (id,)
    ).fetchone()

    if ticket is None:
        abort(404, f"Ticket id {id} doesn't exist.")

    return ticket


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_ticket(id)
    db = get_db()
    db.execute('DELETE FROM ticket WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tickets.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    ticket = get_ticket(id)

    if request.method == 'POST':
        ticket_type = request.form['ticket_type']
        ticket_description = request.form['ticket_description']
        ticketstatus = request.form['ticketstatus']
        promised = request.form['promised']
        error = None

        if not ticket_type:
            error = 'Ticket Type Required.'
        elif not ticket_description:
            error = 'Ticket Description Required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE ticket SET ticket_type = ?, ticket_description = ?, ticketstatus = ?, promised = ?'
                ' WHERE id = ?',
                (ticket_type, ticket_description, ticketstatus, promised, id)
            )
            db.commit()
            return redirect(url_for('tickets.main'))
    
    return render_template('app/ticket/update.html', ticket = ticket)


@bp.route('/<int:id>/complete', methods=('GET', 'POST'))
@login_required
def complete(id):


    return render_template('app/ticket/complete.html', id = id)


@bp.route('/<int:id>/sendout', methods=('GET', 'POST'))
@login_required
def sendout(id):
    ticket = get_ticket(id)

    if request.method == 'POST':
        sentoutlocation = request.form['sentoutlocation']
        sentoutnotes = request.form['sentoutnotes']
        ticketstatus = 'sent out'
        sentoutdate = date.today()
        error = None

        if sentoutlocation is None:
            error = 'Sent Out Location Required'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE ticket SET sentoutlocation = ?, sentoutnotes = ?, ticketstatus = ?, sentoutdate = ?'
                ' WHERE id = ?',
                (sentoutlocation, sentoutnotes, ticketstatus, sentoutdate, id)
            )
            db.commit()
            return redirect(url_for('tickets.main'))

    return render_template('app/ticket/sendout.html', id = id)


@bp.route('/options', methods=('GET', 'POST'))
@login_required
def options():


    return render_template('app/ticket/options')
