
import os
from datetime import date, datetime
import mysqlx
from flask import (
    Blueprint, flash, g, render_template, request
)
from werkzeug.utils import secure_filename

from .auth import login_required
from ..db import db_conf as db

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

class Organization:
    def __init__(self):
        self.errors = []
        self._properties = {
            'Organization_ID': None,    # db primary key
            'Organization_Name': None, 
            'Organization_Initial': None, 
            'Date_Entered': None,
            'Website': None, 
            'Vetted': None,
            'Date_Vetted': None,
            'Risk_Level': None,
            'HQ_Street_Address': None, 
            'HQ_Unit_Apt': None,
            'HQ_City': None, 
            'HQ_Region': None, 
            'HQ_Country': None, 
            'HQ_Zip_Code': None, 
            'Ship_Time': 0,          # Not in db, used to find Ship_Time_In_Days
            'Ship_Time_Unit': None,     # Not in db, used to find Ship_Time_In_Days
            'Ship_Time_In_Days': 0,
            'Roll': None,
            'Documents': [],
            'Notes': None
            }

    def getRoll(self):
        return self._properties['Roll']

    def getOrgData(self):
        self.setShipTimeUnits()
        print(self._properties)
        self._properties['Date_Vetted'] = self._properties['Date_Vetted'].strftime("%d/%m/%y")
        return self._properties

    def getErrors(self):
        return self.errors

    def clearErrors(self):
        self.errors = []

    def queryOrg(self, OrgID):

        # Connection and Query
        session = mysqlx.get_session(
            {'host': db.HOST, 'port': db.PORT, 'user': db.USER, 'password': db.PASSWORD})
        org_schema = session.get_schema('Organizations')
        org_table = org_schema.get_table('Organizations')
        result = org_table.select().where(("Organization_ID = '%s'") % str(OrgID)).execute()
        
        # Get and Order Columns
        column_names = []
        columns = result.get_columns()
        for col in columns:
            column_names.append(col.get_column_name())

        # Get data from db and save in object
        saved_data = result.fetch_one()
        for col in column_names:
            if col == 'Date_Entered':
                self._properties[col] = datetime.strptime(saved_data.get_string(col), db.DATE_FORMAT)
            if col == 'Date_Vetted':
                self._properties[col] = datetime.strptime(saved_data.get_string(col), db.DATE_FORMAT)
            if col == 'Ship_Time_In_Days':
                if saved_data.get_string(col) == 'None':
                    self._properties[col] = 0
                else:
                    self._properties[col] = int(saved_data.get_string(col))
            else:
                self._properties[col] = saved_data.get_string(col)

        return True
    
    def newOrg(self, request_obj, roll):
        formData = dict(request_obj.form)
        # set roll
        self._properties['Roll'] = roll

        # set date entered
        self._properties['Date_Entered'] = str(date.today())

        # set Documents
        #TODO: 
        #print(request_obj['Documents'])

        # set data from form
        form_data = dict(formData)
        form_data_keys = list(form_data.keys())
        for key in form_data_keys:
            if key in self._properties:
                self._properties[key] = form_data[key]
            else:
                self.errors.append("Unknown Key: " + key + "\n")

        # Checks
        self.setShipTime()
        self.checkVettedExpired()
        self.updateVetted()

        # Save Organization in database
        self._saveOrg()
    
    def updateOrg(self, request_obj):
        formData = dict(request_obj.form)

        # update Documents
        #TODO:

        # set data from form
        form_data = dict(formData)
        print(form_data)
        form_data_keys = list(form_data.keys())
        for key in form_data_keys:
            if key in self._properties:
                self._properties[key] = form_data[key]
            else:
                self.errors.append("Unknown Key: " + key + "\n")

        # Checks
        self.setShipTime()
        self.checkVettedExpired()
        self.updateVetted()

        # Save Organization in database
        self._saveOrg()

    def _saveOrg(self):

        # filter data
        columns = (
            'Organization_Name',
            'Organization_Initial',
            'Date_Entered',
            'Website',
            'Vetted',
            'Date_Vetted',
            'Risk_Level',
            'HQ_Street_Address',
            'HQ_Unit_Apt',
            'HQ_City',
            'HQ_Region',
            'HQ_Country',
            'HQ_Zip_Code',
            'Ship_Time_In_Days',
            'Roll',
            'Documents',
            'Notes')
        values_list = []
        for column in columns:
            values_list.append(self._properties[column])
        values = tuple(values_list)

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
            error = "INSERT ITEM ERROR \n"
            error += "Warnings: \n"
            for warning in warnings:
                error += ("    W:" + warning + "\n")
            error += "Attempted Rows Effected: " + rows_effected + "\n"
            error += "Expected Rows Effected: 1 \n"
            self.errors.append(error)
            return False

        # Save Uploaded Files
        if len(self._properties['Documents']) > 0:

            collection = {}

            # Folder Config Settings
            os.chdir(db.UPLOAD_FOLDER)
            uploadFolder = os.path.join(
                os.getcwd(), "organizations/suppliers/", self._properties['Organization_Name'])

            # create a file space in organization collections
            collection.update({"files": []})
            paths = []

            for file in self._properties['Documents']:
                # If the user does not select a file, the browser submits an
                # empty file without a filename.

                if file and db.allowed_file(file.filename):

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
            result = org_coll.add(
                {'_id': int(row_id), 'doc': collection}).execute()

            # IF Err, Report and Rollback
            if warnings != [] and rows_effected != 1:
                session.rollback()
                session.close()
                error = "INSERT DOC ERROR"
                for warning in warnings:
                    error += (warning + "\n")
                self.errors.append(error)
                return False

            for path in paths:
                # Save File
                file.save(path)

        # Commit and close session
        session.commit()
        session.close()
        return True

    def updateVetted(self):
        self._properties['Date_Vetted'] = str(date.today())

    def checkVettedExpired(self):
        #TODO:
        self._properties['Vetted'] = True

    def setShipTime(self):
        time_frame_units = self._properties['Ship_Time_Unit']
        time_frame_amount = self._properties['Ship_Time']
        Ship_Time_In_Days = None
        if time_frame_units == "Day/s":
            Ship_Time_In_Days = time_frame_amount
        elif time_frame_units == "Week/s":
            Ship_Time_In_Days = time_frame_amount * 7
        elif time_frame_units == "Month/s":
            Ship_Time_In_Days = time_frame_amount * 30
        self._properties['Ship_Time_In_Days'] = Ship_Time_In_Days
        return

    def setShipTimeUnits(self):
        self._properties["Ship_Time_Unit"] = "Day/s"
        self._properties["Ship_Time"] = self._properties["Ship_Time_In_Days"]
        if self._properties['Ship_Time_In_Days'] > 30:
            self._properties["Ship_Time_Unit"] = "Month/s"
            self._properties["Ship_Time"] = self._properties["Ship_Time_In_Days"] // 30
            return
        if self._properties['Ship_Time_In_Days'] > 14:
            self._properties["Ship_Time_Unit"] = "Weeks/s"
            self._properties["Ship_Time"] = self._properties["Ship_Time_In_Days"] // 7
            return
        return

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

@bp.route('/create/supplier', methods=('GET', 'POST'))
@login_required
def create_supplier():
    if request.method == 'POST':
        supplier = Organization()
        supplier.newOrg(request, "Supplier")
        errors = supplier.getErrors()

        # Flash Erros if any, else send data to db
        if errors != []:
            for error in errors:
                flash(error)
        else:
            g.header = "Suppliers"
            suppliers()

    return render_template('organizations/create_supplier.html')

@bp.route('/create/client', methods=('GET', 'POST'))
@login_required
def create_client():
    if request.method == 'POST':
        client = Organization()
        client.newOrg(request, "Client")
        errors = client.getErrors()
        
        # Flash Erros if any, else send data to db
        if errors != []:
            for error in errors:
                flash(error)
        else:
            g.header = "Clients"
            clients()
            # return redirect(url_for('organizations.index'))
    return render_template('organizations/create_client.html')

@bp.route('/edit/<int:OrgID>', methods=('GET', 'PUT'))
@login_required
def update(OrgID):

    Org = Organization()
    Org.queryOrg(OrgID)
    Roll = Org.getRoll()

    if request.method == 'GET':
        if Roll == "b'Client'":
            print("Update Client")
            return render_template('organizations/update_client.html',  organizations=Org.getOrgData())
        elif Roll == "b'Supplier'":
            print("Update Supplier")
            return render_template('organizations/update_supplier.html',  organizations=Org.getOrgData())
        else:
            return render_template('home/index.html')

    if request.method == 'PUT':
        Org.updateOrg(request)
        errors = Org.getErrors()

        # Flash Errors if any, else send data to db
        if errors != []:
            for error in errors:
                flash(error)
        else:
            if Org.getRoll() == "b'Supplier'":
                g.header = "Suppliers"
                suppliers()
                # return redirect(url_for('organizations.index'))
            elif Org.getRoll() == "b'Client'":
                g.header = "Clients"
                clients()
                # return redirect(url_for('organizations.index'))

    if Roll == "b'Client'":
        clients()
    elif Roll == "b'Supplier'":
        suppliers()
    else:
        return render_template('home/index.html')

