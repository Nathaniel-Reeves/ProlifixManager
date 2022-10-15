
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


@bp.route('/create/supplier', methods=('GET', 'POST'))
@login_required
def create_supplier():
    if request.method == 'POST':

        # Sort Data
        Organization_Name = request.form['Organization_Name']
        Organization_Initial = request.form['Organization_Initial']

        # Check Errors
        error = None
        if not Organization_Name:
            error = 'Title is required.'

        # Flash Erros if any, else send data to db
        if error is not None:
            flash(error)
        else:
            create(data)
            g.header = "Suppliers"
            return redirect(url_for('organizations.index'))
    return render_template('organizations/create_supplier.html')


@bp.route('/create/client', methods=('GET', 'POST'))
@login_required
def create_client():
    if request.method == 'POST':

       # Sort Data
        Organization_Name = request.form['Organization_Name']
        Organization_Initial = request.form['Organization_Initial']

        # Check Errors
        error = None
        if not Organization_Name:
            error = 'Title is required.'

        # Flash Erros if any, else send data to db
        if error is not None:
            flash(error)
        else:
            create(data)
            g.header = "Clients"
            return redirect(url_for('organizations.index'))
    return render_template('organizations/create_client.html')


def create(data):
    db = DatabaseConnection()
    session = db.get_session()
    session.sql(
        '''INSERT INTO `Organizations`.`Organizations` (`Organization_Name`, `Organization_Initial`, `Website`, `HQ_Street_Address`, `HQ_Unit-Apt`, 
        `HQ_City`, `HQ_Region`, `HQ_Country`, `HQ_Zip_Code`, `Country_Origin`, `Ship_Time_In_Days`, `Roll`) 
        
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
    ).bind(data).execute()
    session.commit()
    return True


