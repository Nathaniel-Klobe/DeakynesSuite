from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.database import get_db

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/')
def main():
    db = get_db()
    orders = db.execute(
        'SELECT o.id, c.last_name, c.phone, order_type, order_description, order_from, created, promised'
        ' FROM specialorder o JOIN customer c ON o.customer_id = c.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('app/order/orders.html', orders = orders)



@bp.route('/landing', methods=('GET', 'POST'))
@login_required
def customer_landing():
    if request.method == "POST":
        if request.form.get('create'):
            return redirect(url_for('orders.new_customer'))

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
                return redirect(url_for('orders.create', id = customer['id']))

    return render_template('app/customer_landing.html')


@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    if request.method == 'POST':
        order_type = request.form['order_type']
        order_description = request.form['order_description']
        order_from = request.form['order_from']
        promised = request.form['promised']
        created = datetime.now()
        customer_id = id
        error = None

        if not order_type:
            error = 'Order Type Required.'
        elif not order_description:
            error = 'Order Description Required.'
        elif not order_from:
            error = 'Order From Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO specialorder (customer_id, order_type, order_description, order_from, created, promised) VALUES(?, ?, ?, ?, ?, ?)',
                (customer_id, order_type, order_description, order_from, created, promised) 
            )
            db.commit()
            return redirect(url_for('orders.main'))

    return render_template('app/order/create.html', id = id)


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
            return redirect(url_for('orders.create', id = customer_id))
    return render_template('app/customer/create.html')


def get_order(id):
    order = get_db().execute(
        'SELECT o.id, c.last_name, c.phone, order_type, order_description, order_from, created, promised'
        ' FROM specialorder o JOIN customer c ON o.customer_id = c.id'
        ' WHERE o.id = ?', (id,)
    ).fetchone()

    if order is None:
        abort(404, f"Order id {id} doesn't exist.")

    return order


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_order(id)
    db = get_db()
    db.execute('DELETE FROM specialorder WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('orders.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    order = get_order(id)

    if request.method == 'POST':
        order_type = request.form['order_type']
        order_description = request.form['order_description']
        order_from = request.form['order_from']
        promised = request.form['promised']
        error = None

        if not order_type:
            error = 'Order Type Required.'
        elif not order_description:
            error = 'Order Description Required.'
        elif not order_from:
            error = 'Order From Required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE specialorder SET order_type = ?, order_description = ?, order_from = ?, promised = ?'
                ' WHERE id = ?',
                (order_type, order_description, order_from, promised, id)
            )
            db.commit()
            return redirect(url_for('orders.main'))
    
    return render_template('app/order/update.html', order = order)