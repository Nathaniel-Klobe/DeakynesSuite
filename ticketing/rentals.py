from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.db import get_db

bp = Blueprint('rentals', __name__, url_prefix='/rentals')

@bp.route('/')
def main():
    db = get_db()
    rentals = db.execute(
        'SELECT r.id, c.last_name, c.phone, rentalitem, rental_period, cost, paid, created, promised'
        ' FROM rental r JOIN customer c ON r.customer_id = c.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('app/rental/rentals.html', rentals = rentals)


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
                return redirect(url_for('rentals.create', id = customer['id']))

    return render_template('app/customer_landing.html')


@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    db = get_db()
    rental_list = db.execute(
        'SELECT item_name FROM rentalitem'
    ).fetchall()
    if request.method == 'POST':
        rentalitem = request.form['rentalitem']
        rental_period = request.form['rental_period']
        cost = request.form['cost']
        paid = request.form['paid']
        promised = request.form['promised']
        created = datetime.now()
        customer_id = id
        error = None

        if not rentalitem:
            error = 'Rental Item Required.'
        elif not rental_period:
            error = 'Rental Period Required.'
        elif not cost:
            error = 'Cost Required.'
        elif not paid:
            error = 'Has Paid Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO rental (customer_id, rentalitem, rental_period, cost, paid, created, promised) VALUES(?, ?, ?, ?, ?, ?, ?)',
                (customer_id, rentalitem, rental_period, cost, paid, created, promised) 
            )
            db.commit()
            return redirect(url_for('rental.main'))

    return render_template('app/rental/create.html', id = id, rental_list = rental_list)


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
            return redirect(url_for('rentals.create', id = customer_id))
    return render_template('app/customer/create.html')


def get_rental(id):
    rental = get_db().execute(
        'SELECT r.id, c.last_name, c.phone, rentalitem, rental_period, cost, paid, created, promised'
        ' FROM rental r JOIN customer c ON r.customer_id = c.id'
        ' WHERE r.id = ?', (id,)
    ).fetchone()

    if rental is None:
        abort(404, f"Rental id {id} doesn't exist.")

    return rental


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_rental(id)
    db = get_db()
    db.execute('DELETE FROM rental WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('rentals.main'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    rental_list = db.execute(
        'SELECT item_name FROM rentalitem'
    ).fetchall()
    rental = get_rental(id)

    if request.method == 'POST':
        rentalitem = request.form['rentalitem']
        rental_period = request.form['rental_period']
        cost = request.form['cost']
        paid = request.form['paid']
        promised = request.form['promised']
        error = None

        if not rentalitem:
            error = 'Rental Item Required.'
        elif not rental_period:
            error = 'Rental Period Required.'
        elif not cost:
            error = 'Cost Required.'
        elif not paid:
            error = 'Has Paid Required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE rental SET rentalitem = ?, rental_period = ?, cost = ?, paid = ?, promised = ?'
                ' WHERE id = ?',
                (rentalitem, rental_period, cost, paid, promised, id)
            )
            db.commit()
            return redirect(url_for('rentals.main'))
    
    return render_template('app/rental/update.html', rental = rental, rental_list = rental_list)


@bp.route('/rentalitems')
@login_required
def rentalitems():
    db = get_db()
    rentalitems = db.execute(
        'SELECT * FROM rentalitem'
    ).fetchall()

    return render_template('app/rental/rentalitems.html', rentalitems = rentalitems)


@bp.route('/createitem', methods=('GET', 'POST'))
@login_required
def createitem():
    if request.method == 'POST':
        item_name = request.form['rentalitem']
        sku = request.form['sku']
        item_description = request.form['item_description']
        error = None

        if item_name is None:
            error = 'Item Name Required.'
        elif sku is None:
            error = 'Sku Required.'
        elif item_description is None:
            error = 'Item Description Required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO rentalitem (item_name, sku, item_description) VALUES (?, ?, ?)',
                (item_name, sku, item_description)
            )
            db.commit()
            return redirect(url_for('rentals.rentalitems'))

    return render_template('app/rental/createitem.html')


def get_rentalitem(id):
    rentalitem = get_db().execute(
        'SELECT id, item_name, sku, item_description'
        ' FROM rentalitem'
        ' WHERE id = ?', (id,)
    ).fetchone()

    if rentalitem is None:
        abort(404, f"Rental Item id {id} doesn't exist.")

    return rentalitem


@bp.route('/<int:id>/item/delete', methods=('POST',))
@login_required
def deleteitem(id):
    get_rentalitem(id)
    db = get_db()
    db.execute('DELETE FROM rentalitem WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('rentalitems.main'))


@bp.route('/<int:id>/item/update', methods=('GET', 'POST'))
@login_required
def updateitem(id):
    rentalitem = get_rentalitem(id)

    if request.method == 'POST':
        item_name = request.form['rentalitem']
        sku = request.form['sku']
        item_description = request.form['item_description']
        error = None

        if not item_name:
            error = 'Rental Item Required.'
        elif not sku:
            error = 'Rental Period Required.'
        elif not item_description:
            error = 'Cost Required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE rentalitem SET item_name = ?, sku = ?, item_description = ?'
                ' WHERE id = ?',
                (item_name, sku, item_description)
            )
            db.commit()
            return redirect(url_for('rentalitems.main'))
    
    return render_template('app/rental/updateitem.html', rentalitem = rentalitem)