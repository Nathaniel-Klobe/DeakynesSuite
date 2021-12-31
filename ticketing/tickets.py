from datetime import date, datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy.sql.expression import false

from werkzeug.exceptions import abort

from ticketing.database import db_session
from ticketing.auth import login_required
from ticketing.models import Ticket

bp = Blueprint('tickets', __name__, url_prefix='/tickets')

@bp.route('/')
def main():
    tickets = db_session.query()
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
        promised = request.form['promised']
        error = None

        if not ticket_type:
            error = 'Ticket Type Required.'
        elif not ticket_description:
            error = 'Ticket Description Required.'

        if error is not None:
            flash(error)
        else:
            db_session.add(Ticket(id, ticket_type=ticket_type,
                ticket_description=ticket_description, ticket_status='New', created=datetime.now(),
                promised=promised, bDone=False, bNotified=False,
                bRetrieved=False ))

            db_session.commit()
            return redirect(url_for('tickets.main'))

    return render_template('app/ticket/create.html', id = id)


def get_ticket(id):
    ticket = Ticket.query.filter(Ticket.id == 'id').first()
    return ticket


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    ticket = get_ticket(id)
    db_session.delete(ticket)
    return redirect(url_for('tickets.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    ticket = get_ticket(id)

    if request.method == 'POST':
        ticket_type = request.form['ticket_type']
        ticket_description = request.form['ticket_description']
        ticketstatus = request.form.get('ticketstatus')
        promised = request.form['promised']
        error = None

        if ticketstatus is not None:
            ticketstatus = 'In Progress'

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
    ticket = get_ticket(id)

    if request.method == 'POST':
        labor = request.form['labor']
        parts = request.form['parts']
        other = request.form['other']
        notes = request.form['notes']
        hascalled = request.form.get('called')
        haspickedup = request.form.get('pickedup')
        ticketstatus = 'completed'
        completed = date.today()
        total = labor + parts + other
        called = None
        pickedup = None
        error = None

        if hascalled is not None:
            ticketstatus = 'called'
            called = date.today()

        if haspickedup is not None:
            ticketstatus = 'picked up'
            pickedup = date.today()
        
        if labor is None:
            error = 'Labor Cost Required.'
        elif parts is None:
            error = 'Parts Cost Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE ticket SET labor = ?, parts = ?, other = ?, total = ?, notes = ?, called = ?, pickedup = ?, completed = ?, ticketstatus = ?'
                ' WHERE id = ?',
                (labor, parts, other, total, notes, called, pickedup, completed, ticketstatus, id)
            )
            db.commit()
            return redirect(url_for('tickets.main'))

    return render_template('app/ticket/complete.html', id = id, ticket = ticket)


@bp.route('/<int:id>/view')
@login_required
def view(id):
    ticket = get_ticket(id)

    return render_template('app/ticket/view.html', ticket = ticket)

@bp.route('/options', methods=('GET', 'POST'))
@login_required
def options():


    return render_template('app/ticket/options')
