from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.db import get_db

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
            db.execute(
                'INSERT INTO customer (first_name, last_name, street_address, phone) VALUES(?, ?, ?, ?)',
                (first_name, last_name, street_address, phone)
            )
            db.commit()
            return redirect(url_for('customers.main'))
    return render_template('app/customer/create.html')
