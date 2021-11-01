from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from ticketing.auth import login_required
from ticketing.db import get_db

bp = Blueprint('rentalitems', __name__, url_prefix='/rentalitems')

@bp.route('/')
def main():
    pass