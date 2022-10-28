
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


@bp.route('/create/supplier', methods=('GET', 'POST', 'PUT'))
@login_required
def create_supplier():
    if request.method == 'POST':

       # Sort Data
        Organization_Name = request.form['Organization_Name']
        Organization_Initial = request.form['Organization_Initial']
        data = dict(request.form)

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
            suppliers()
    return render_template('organizations/create_supplier.html')


@bp.route('/create/client', methods=('GET', 'POST', 'PUT'))
@login_required
def create_client():
    if request.method == 'POST':

       # Sort Data
        Organization_Name = request.form['Organization_Name']
        Organization_Initial = request.form['Organization_Initial']
        data = dict(request.form)
        #files = dict(request.files)
        

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
            clients()
            # return redirect(url_for('organizations.index'))
    return render_template('organizations/create_client.html')


def create(data):
    print(data)

    time_frame_units = data.pop('Ship_Time_Unit')
    time_frame_amount = int(data.pop('Ship_Time'))
    Ship_Time_In_Days = 0
    if time_frame_units == "Day/s":
        Ship_Time_In_Days = time_frame_amount
    elif time_frame_units == "Week/s":
        Ship_Time_In_Days = time_frame_amount * 7
    elif time_frame_units == "Month/s":
        Ship_Time_In_Days = time_frame_amount * 30

    data['Ship_Time_In_Days'] = Ship_Time_In_Days


    columns = tuple(data.keys())
    values = tuple(data.values())


    print(columns)
    print(values)

    db = DatabaseConnection()
    session = db.get_session()
    org_schema = session.get_schema('Organizations')
    org_table = org_schema.get_table('Organizations')
    org_table.insert(columns).values(values).execute()
    session.commit()

    return True


