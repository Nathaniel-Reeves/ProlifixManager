"""
Handling api requests related to Organization objects.  Defines organization
objects.
"""

import os
from datetime import date, datetime
import mysqlx
from flask import (Blueprint, flash, g, render_template, request)
from werkzeug.utils import secure_filename

from .auth import login_required
from ..db import db_conf as db

bp = Blueprint('organizations', __name__, url_prefix='/organizations')


class Organization:
    """
    Class representing a organization or company.  Contains company name and 
    initials, address, website, and other information relevent to the needs
    of this MRP system.
    """

    def __init__(self, Organization_ID=None):
        self.errors = []

        # Organization Attributes
        self.Organization_ID = Organization_ID
        self.Organization_Name = ""
        self.Organization_Initial = ""
        self.Date_Entered = None
        self.Website = ""
        self.Vetted = False
        self.Date_Vetted = None
        self.Risk_Level = "UNKNOWN"
        self.HQ_Street_Address = ""
        self.HQ_Unit_Apt = ""
        self.HQ_City = ""
        self.HQ_Region = ""
        self.HQ_Country = ""
        self.HQ_Zip_Code = ""
        self.Ship_Time = 0
        self.Ship_Time_Unit = 1
        self.Ship_Time_In_Days = 0
        self.Prolifix = False
        self.Supplier = False
        self.Client = False
        self.Documents = []
        self.Notes = ""

        self.rawFiles = {}

        # Child Attributes
        self.People = []
        self.Prooducts = []
        self.Purchase_Orders = []

        # If Organization_ID query db
        if self.Organization_ID:
            self.query_org(self.Organization_ID)

    def get_errors(self):
        """Returns error list."""
        return self.errors

    def clear_errors(self):
        "Clears error list."
        self.errors = []

    def query_org(self, OrgID):

        # Connection and Query
        session = mysqlx.get_session({
            'host': db.HOST,
            'port': db.PORT,
            'user': db.USER,
            'password': db.PASSWORD
        })
        org_schema = session.get_schema('Organizations')
        org_table = org_schema.get_table('Organizations')
        result = org_table.select().where(
            ("Organization_ID = '%s'") % str(OrgID)).execute()

        # Get data from db and save in object
        self.Organization_ID = result.index_of("Organization_ID")
        self.Organization_Name = result.index_of("Organization_Name")
        self.Organization_Initial = result.index_of("Organization_Initial")
        self.Date_Entered = result.index_of("Date_Entered")
        self.Website = result.index_of("Website")
        self.Vetted = result.index_of("Vetted")
        self.Date_Vetted = result.index_of("Date_Vetted")
        self.HQ_Street_Address = result.index_of("HQ_Street_Address")
        self.HQ_Unit_Apt = result.index_of("HQ_Unit_Apt")
        self.HQ_City = result.index_of("HQ_City")
        self.HQ_Region = result.index_of("HQ_Region")
        self.HQ_Country = result.index_of("HQ_Country")
        self.HQ_Zip_Code = result.index_of("HQ_Zip_Code")
        self.Ship_Time = result.index_of("Ship_Time")
        self.Ship_Time_Unit = result.index_of("Ship_Time_Unit")
        self.Ship_Time_In_Days = result.index_of("Ship_Time_In_Days")
        self.Prolifix = result.index_of("Prolifix")
        self.Supplier = result.index_of("Supplier")
        self.Client = result.index_of("Client")
        self.Notes = result.index_of("Notes")

        self._get_Org_Docs(OrgID)

        return True

    def _get_Org_Docs(self, OrgID):
        session = mysqlx.get_session({
            'host': db.HOST,
            'port': db.PORT,
            'user': db.USER,
            'password': db.PASSWORD
        })
        org_schema = session.get_schema('Organizations')
        org_coll = org_schema.get_collection('OrganizationDocs')
        documents = org_coll.get_one(OrgID)
        if not documents:
            self.Documents = []
            return False
        print(documents)
        print("RUNNING")

    def __str__(self):
        return_str = "<"
        return_str += "Org_ID = " + str(self.Organization_ID) + " | "
        return_str += "Org_Name = " + str(self.Organization_Name) + " | "
        return_str += "Org_Initial = " + str(self.Organization_Initial)
        return_str += ">"
        return return_str

    def __dict__(self):
        return self.obj_to_dict()

    def obj_to_dict(self):
        return_dict = {}
        return_dict["Organization_ID"] = self.Organization_ID
        return_dict["Organization_Name"] = self.Organization_Name
        return_dict["Organization_Initial"] = self.Organization_Initial
        return_dict["Date_Entered"] = self.Date_Entered
        return_dict["Website"] = self.Website
        return_dict["Vetted"] = self.Vetted
        return_dict["Date_Vetted"] = self.Date_Vetted
        return_dict["HQ_Street_Address"] = self.HQ_Street_Address
        return_dict["HQ_Unit_Apt"] = self.HQ_Unit_Apt
        return_dict["HQ_City"] = self.HQ_City
        return_dict["HQ_Region"] = self.HQ_Region
        return_dict["HQ_Country"] = self.HQ_Country
        return_dict["HQ_Zip_Code"] = self.HQ_Zip_Code
        return_dict["Ship_Time"] = self.Ship_Time
        return_dict["Ship_Time_Unit"] = self.Ship_Time_Unit
        return_dict["Ship_Time_In_Days"] = self.Ship_Time_In_Days
        return_dict["Prolifix"] = self.Prolifix
        return_dict["Supplier"] = self.Supplier
        return_dict["Client"] = self.Client
        return_dict["Notes"] = self.Notes
        return return_dict

    def new_org(self, request_obj):

        # set Data
        request_data = request_obj.form
        self.Date_Entered = str(date.today())
        self.Organization_Name = request_data["Organization_Name"]
        self.Organization_Initial = request_data["Organization_Initial"]
        self.Website = request_data["Website"]
        self.Date_Vetted = request_data["Date_Vetted"]
        self.Risk_Level = request_data["Risk_Level"]
        self.HQ_Street_Address = request_data["HQ_Street_Address"]
        self.HQ_Unit_Apt = request_data["HQ_Unit_Apt"]
        self.HQ_City = request_data["HQ_City"]
        self.HQ_Region = request_data["HQ_Region"]
        self.HQ_Country = request_data["HQ_Country"]
        self.HQ_Zip_Code = request_data["HQ_Zip_Code"]
        self.Ship_Time = request_data["Ship_Time"]
        self.Ship_Time_Unit = request_data["Ship_Time_Unit"]

        self.Prolifix = request_data["Prolifix"]
        self.Supplier = request_data["Supplier"]
        self.Client = request_data["Client"]

        self.Notes = request_data["Notes"]

        # set Documents
        if request_obj.files:
            self.rawFiles = request_obj.files.values()

        # Validation Checks
        self._set_ship_time()
        self.check_vetted_expired()
        self.update_vetted()

        # Save Organization in database
        self._save_org()

    def update_org(self, request_obj):
        formData = dict(request_obj.form)

        # update Documents
        #TODO:

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
        self.check_vetted_expired()
        self.update_vetted()

        # Save Organization in database
        self._save_org()

    def _save_org(self):
        # Start session and transaction
        session = mysqlx.get_session({
            'host': db.HOST,
            'port': db.PORT,
            'user': db.USER,
            'password': db.PASSWORD
        })
        session.start_transaction()

        # Get Schema and table
        org_schema = session.get_schema('Organizations')
        org_table = org_schema.get_table('Organizations')

        # Save Data
        obj_data = self.obj_to_dict()
        columns = tuple(obj_data.keys())
        values = tuple(obj_data.values())
        result = org_table.insert(columns).values(values).execute()

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
        if self.rawFiles:

            # Folder Config Settings
            os.chdir(db.UPLOAD_FOLDER)
            uploadFolder = os.path.join(os.getcwd(),
                                        "organizations/suppliers/",
                                        self.Organization_Name)

            # create a file space in organization collections
            collection = {}
            collection.update({"files": []})

            for file in self.rawFiles:
                # If the user does not select a file, the browser submits an
                # empty file without a filename.

                if file and db.allowed_file(file.filename):

                    # Compile file tree/path
                    filename = secure_filename(file.filename)
                    path = os.path.join(uploadFolder, filename)

                    # Create file tree/path if it doesn't exist already
                    if not os.path.exists(uploadFolder):
                        os.makedirs(uploadFolder)

                    # save Path to Documents
                    self.Documents.append(path)

                    # create file link in organization collection
                    collection["files"].append({
                        "date": str(datetime.today()),
                        "path": path
                    })

            # Create Collection if none exists
            #org_coll = org_schema.create_collection('OrganizationDocs', True)

            # Get Collection
            org_coll = org_schema.get_collection('OrganizationDocs',
                                                 check_existence=True)

            # Save file paths
            result = org_coll.add({
                'Documents_id': int(row_id),
                'doc': collection
            }).execute()

            # IF Err, Report and Rollback
            if warnings != [] and rows_effected != 1:
                session.rollback()
                session.close()
                error = "INSERT DOC ERROR"
                for warning in warnings:
                    error += (warning + "\n")
                self.errors.append(error)
                return False

            for path in self.Documents:
                # Save File
                file.save(path)

        # Commit and close session
        session.commit()
        session.close()
        return True

    def update_vetted(self):
        self.Date_Vetted = str(date.today())

    def check_vetted_expired(self):
        #TODO:
        self.Vetted = True

    def _set_ship_time(self):
        if self.Ship_Time_Unit == "Day/s":
            self.Ship_Time_In_Days = self.Ship_Time
        elif self.Ship_Time_Unit == "Week/s":
            self.Ship_Time_In_Days = self.Ship_Time * 7
        elif self.Ship_Time_Unit == "Month/s":
            self.Ship_Time_In_Days = self.Ship_Time * 30
        else:
            self.Ship_Time_In_Days = self.Ship_Time
        return


@bp.route('/clients', methods=('GET', ))
@login_required
def clients():
    session = mysqlx.get_session({
        'host': db.HOST,
        'port': db.PORT,
        'user': db.USER,
        'password': db.PASSWORD
    })
    clients = session.sql(
        """SELECT * FROM `Organizations`.`Organizations` WHERE `Client` = true ORDER BY `Organization_Name` DESC;"""
    ).execute()
    g.orgtype = "client"
    clients = clients.fetch_all()
    return render_template('organizations/read-org.html',
                           organizations=clients)


@bp.route('/suppliers', methods=('GET', ))
@login_required
def suppliers():
    session = mysqlx.get_session({
        'host': db.HOST,
        'port': db.PORT,
        'user': db.USER,
        'password': db.PASSWORD
    })
    suppliers = session.sql(
        """SELECT * FROM `Organizations`.`Organizations` WHERE `Supplier` = true ORDER BY `Organization_Name` DESC;"""
    ).execute()
    g.orgtype = "supplier"
    suppliers = suppliers.fetch_all()
    return render_template('organizations/read-org.html',
                           organizations=suppliers)


@bp.route('/create/<string:org_type>', methods=('GET', 'POST'))
@login_required
def create(org_type):

    # Stop new entry for Prolifix
    if org_type == "Prolifix":
        return render_template('organizations/create-org.html')

    g.orgtype = org_type

    if request.method == 'POST':
        org = Organization()
        org.new_org(request)
        errors = org.get_errors()

        # Flash Erros if any, else send data to db
        if errors != []:
            for error in errors:
                flash(error)
        else:
            if org_type == "client":
                clients()
            else:
                suppliers()

    return render_template('organizations/create-org.html')


@bp.route('/update/<int:OrgID>', methods=('GET', 'PUT'))
@login_required
def update(OrgID):

    org = Organization()
    org.query_org(OrgID)

    # Prevent prolifix entry from being edited.
    if org.Organization_Name == "Prolifix Nutrition":
        return render_template('home/index.html')

    if request.method == 'GET':
        if org.Supplier:
            print("Update Client")
            return render_template('organizations/update-org.html',
                                   organizations=Org.obj_to_dict())

    if request.method == 'PUT':
        org.update_org(request)
        errors = org.get_errors()

        # Flash Errors if any, else send data to db
        if errors != []:
            for error in errors:
                flash(error)

    if org.Supplier:
        suppliers()
    elif org.Client:
        clients()
    else:
        return render_template('home/index.html')
