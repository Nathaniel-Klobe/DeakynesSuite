from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.db import get_db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    db = get_db()
    cTickets = db.execute(
        'SELECT COUNT(*) FROM ticket'
    ).fetchone()[0]
    cOrders = db.execute(
        'SELECT COUNT(*) FROM specialorder'
    ).fetchone()[0]
    cRentals = db.execute(
        'SELECT COUNT(*) FROM rental'
    ).fetchone()[0]

    return render_template('app/index.html', 
        cTickets = cTickets, cOrders = cOrders, cRentals = cRentals)

    