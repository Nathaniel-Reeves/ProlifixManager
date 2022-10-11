
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import login_required
from ..db import DatabaseConnection

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@bp.route('/clients', methods=('GET',))
@login_required
def clients():
    db = DatabaseConnection()
    session = db.get_session()
    clients = session.sql(
        """SELECT * FROM `Organizations`.`Organizations` WHERE Roll = 'Client' ORDER BY `Organization_Name` DESC;"""
    ).execute()
    clients = clients.fetch_all()
    g.header = "Clients"
    return render_template('organizations/index.html', organizations=clients)

@bp.route('/suppliers', methods=('GET',))
@login_required
def suppliers():
    db = DatabaseConnection()
    session = db.get_session()
    suppliers = session.sql(
        """SELECT * FROM `Organizations`.`Organizations` WHERE Roll = 'Supplier' ORDER BY `Organization_Name` DESC;"""
    ).execute()
    g.header = "Suppliers"
    suppliers = suppliers.fetch_all()
    return render_template('organizations/index.html', organizations=suppliers)