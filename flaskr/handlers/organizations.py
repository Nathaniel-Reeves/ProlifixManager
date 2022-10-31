
import functools
import os
from datetime import date, datetime, timedelta
import json
import mysqlx


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .auth import login_required
from ..db import db_conf as db


bp = Blueprint('organizations', __name__, url_prefix='/organizations')


@bp.route('/clients', methods=('GET',))
@login_required
def clients():
    session = mysqlx.get_session(
        {'host': db.HOST, 'port': db.PORT, 'user': db.USER, 'password': db.PASSWORD})
    clients = session.sql(
        """SELECT * FROM `Organizations`.`Organizations` WHERE Roll = 'Client' ORDER BY `Organization_Name` DESC;"""
    ).execute()
    clients = clients.fetch_all()
    g.header = "Clients"
    return render_template('organizations/index.html', organizations=clients)

@bp.route('/suppliers', methods=('GET',))
@login_required
def suppliers():
    session = mysqlx.get_session(
        {'host': db.HOST, 'port': db.PORT, 'user': db.USER, 'password': db.PASSWORD})
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
        Date_Vetted = datetime.strptime(request.form['Date_Vetted'],"%Y-%m-%d").date()
        Risk_Level = request.form['Risk_Level']

        data = dict(request.form)
        data['Vetted'] = 0
        data['Roll'] = 3

        data = setShipTime(data)

        for k in data:
            if data[k] == "":
                data[k] = None

        files = request.files

        # Check Errors
        error = None
        if not Organization_Name:
            error = 'Company Name is required.'
        if not Organization_Initial:
            error = 'Company Initials are required.'

        # Check Vetted
        if checkVettedExpired(Date_Vetted, Risk_Level):
            data['Vetted'] = 0

        # Flash Erros if any, else send data to db
        if error is not None:
            flash(error)
        else:
            fileCreated = create(data, files)
            if not fileCreated:
                flash("500 INTERNAL SERVER ERR - Supplier Not Saved")
            else:
                flash(Organization_Name + " was succesfuly saved!")

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


def create(data, files):

    columns = tuple(data.keys())
    values = tuple(data.values())

    # Start session and transaction
    session = mysqlx.get_session(
        {'host': db.HOST, 'port': db.PORT, 'user': db.USER, 'password': db.PASSWORD})
    session.start_transaction()

    # Save Data
    org_schema = session.get_schema('Organizations')
    org_table = org_schema.get_table('Organizations')
    result = org_table.insert(
        columns).values(values).execute()

    # Save Statement Results
    row_id = result.get_autoincrement_value()
    warnings = result.get_warnings()
    rows_effected = result.get_affected_items_count()

    # IF Err, Report and Rollback
    if warnings != [] and rows_effected != 1:
        session.rollback()
        session.close()
        print("INSERT ITEM ERROR")
        print("Warnings: ")
        for warning in warnings:
            print("    W:", warning)
        print("Attempted Rows Effected: ", rows_effected)
        print("Expected Rows Effected: 1")
        return False

    # Save Uploaded Files
    if len(files) != 0:

        collection = {}

        # Sort out files into a python list
        files = list(request.files.to_dict().values())

        # Folder Config Settings
        os.chdir(db.UPLOAD_FOLDER)
        uploadFolder = os.path.join(
            os.getcwd(), "organizations/suppliers/", data['Organization_Name'])

        # create a file space in organization collections
        collection.update({"files": []})
        paths = []

        for file in files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.

            if file and allowed_file(file.filename):

                # Compile file tree/path
                filename = secure_filename(file.filename)
                path = os.path.join(uploadFolder, filename)

                # Create file tree/path if it doesn't exist already
                if not os.path.exists(uploadFolder):
                    os.makedirs(uploadFolder)

                # Store File Path
                paths.append(path)

                # create file link in organization collection
                collection["files"].append(
                        {"date": str(datetime.today()), "path": path})

        # Create Collection if none exists
        org_coll = org_schema.create_collection('OrganizationDocs', True)

        # Save file paths
        result = org_coll.add({'_id': int(row_id), 'doc':collection}).execute()

        # IF Err, Report and Rollback
        if warnings != [] and rows_effected != 1:
            session.rollback()
            session.close()
            print("INSERT DOC ERROR")
            for warning in warnings:
                print(warning)
            return False

        for path in paths:
            # Save File
            file.save(path)

    # Commit and close session
    session.commit()
    session.close()
    return True

def allowed_file(filename, allowed_extensions=db.ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def checkVettedExpired(date, riskLevel):
    today = date.today()
    if riskLevel == "No Risk":
        return True
    elif riskLevel == "Low Risk":
        # check/vet every five years
        years_ago = today - timedelta(days = 1825)
    elif riskLevel == "Medium Risk":
        # check/vet every three years
        years_ago = today - timedelta(days = 1095)
    elif riskLevel == "High Risk":
        # check/vet every year
        years_ago = today - timedelta(days = 365)
    else:
        return False

    if date > today:
        return True 
    return False

def setShipTime(data):
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
    return data
