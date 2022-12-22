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
    """Represents an organization or company.

    Contains company name and initials, address, website, and other
    information relevent to the needs of this MRP system.

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, organization_id=None):
        self.errors = []

        # Organization Attributes
        self.organization_id = organization_id
        self.organization_name = ""
        self.organization_initial = ""
        self.date_entered = None
        self.website = ""
        self.vetted = False
        self.date_vetted = None
        self.risk_level = "UNKNOWN"
        self.hq_street_address = ""
        self.hq_unit_apt = ""
        self.hq_city = ""
        self.hq_region = ""
        self.hq_country = ""
        self.hq_zip_code = ""
        self.ship_time = 0
        self.ship_time_unit = 1
        self.ship_time_in_days = 0
        self.prolifix = False
        self.supplier = False
        self.client = False
        self.documents = []
        self.notes = ""

        self.raw_files = {}

        # If organization_id query db
        if self.organization_id:
            self.query_org(self.organization_id)

    def get_errors(self):
        """Returns error list."""
        return self.errors

    def clear_errors(self):
        "Clears error list."
        self.errors = []

    def query_org(self, org_id):

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
            (f"Organization_ID = '%s'") % str(org_id)).execute()

        # Get data from db and save in object
        self.organization_id = result.index_of("organization_id")
        self.organization_name = result.index_of("Organization_Name")
        self.organization_initial = result.index_of("Organization_Initial")
        self.date_entered = result.index_of("Date_Entered")
        self.website = result.index_of("Website")
        self.vetted = result.index_of("Vetted")
        self.date_vetted = result.index_of("Date_Vetted")
        self.hq_street_address = result.index_of("HQ_Street_Address")
        self.hq_unit_apt = result.index_of("HQ_Unit_Apt")
        self.hq_city = result.index_of("HQ_City")
        self.hq_region = result.index_of("HQ_Region")
        self.hq_country = result.index_of("HQ_Country")
        self.hq_zip_code = result.index_of("HQ_Zip_Code")
        self.ship_time = result.index_of("Ship_Time")
        self.ship_time_unit = result.index_of("Ship_Time_Unit")
        self.ship_time_in_days = result.index_of("Ship_Time_In_Days")
        self.prolifix = result.index_of("Prolifix")
        self.supplier = result.index_of("Supplier")
        self.client = result.index_of("Client")
        self.notes = result.index_of("Notes")

        self._get_org_docs(org_id)

        return True

    def _get_org_docs(self, org_id):
        session = mysqlx.get_session({
            'host': db.HOST,
            'port': db.PORT,
            'user': db.USER,
            'password': db.PASSWORD
        })
        org_schema = session.get_schema('Organizations')
        org_coll = org_schema.get_collection('OrganizationDocs')
        documents = org_coll.get_one(org_id)
        if not documents:
            self.documents = []
            return False
        print(documents)
        print("RUNNING")
        return True

    def __str__(self):
        return_str = "<"
        return_str += "Org_ID = " + str(self.organization_id) + " | "
        return_str += "Org_Name = " + str(self.organization_name) + " | "
        return_str += "Org_Initial = " + str(self.organization_initial)
        return_str += ">"
        return return_str

    def __dict__(self):
        return self.obj_to_dict()

    def obj_to_dict(self):
        return_dict = {}
        return_dict["Organization_ID"] = self.organization_id
        return_dict["Organization_Name"] = self.organization_name
        return_dict["Organization_Initial"] = self.organization_initial
        return_dict["Date_Entered"] = self.date_entered
        return_dict["Website"] = self.website
        return_dict["Vetted"] = self.vetted
        return_dict["Date_Vetted"] = self.date_vetted
        return_dict["HQ_Street_Address"] = self.hq_street_address
        return_dict["HQ_Unit_Apt"] = self.hq_unit_apt
        return_dict["HQ_City"] = self.hq_city
        return_dict["HQ_Region"] = self.hq_region
        return_dict["HQ_Country"] = self.hq_country
        return_dict["HQ_Zip_Code"] = self.hq_zip_code
        return_dict["Ship_Time"] = self.ship_time
        return_dict["Ship_Time_Unit"] = self.ship_time_unit
        return_dict["Ship_Time_In_Days"] = self.ship_time_in_days
        return_dict["Prolifix"] = self.prolifix
        return_dict["Supplier"] = self.supplier
        return_dict["Client"] = self.client
        return_dict["Notes"] = self.notes
        return return_dict

    def new_org(self, request_obj):

        # set Data
        request_data = request_obj.form
        self.date_entered = str(date.today())
        self.organization_name = request_data["Organization_Name"]
        self.organization_initial = request_data["Organization_Initial"]
        self.website = request_data["Website"]
        self.date_vetted = request_data["Date_Vetted"]
        self.risk_level = request_data["Risk_Level"]
        self.hq_street_address = request_data["HQ_Street_Address"]
        self.hq_unit_apt = request_data["HQ_Unit_Apt"]
        self.hq_city = request_data["HQ_City"]
        self.hq_region = request_data["HQ_Region"]
        self.hq_country = request_data["HQ_Country"]
        self.hq_zip_code = request_data["HQ_Zip_Code"]
        self.ship_time = request_data["Ship_Time"]
        self.ship_time_unit = request_data["Ship_Time_Unit"]

        self.prolifix = request_data["Prolifix"]
        self.supplier = request_data["Supplier"]
        self.client = request_data["Client"]

        self.notes = request_data["Notes"]

        # set Documents
        if request_obj.files:
            self.raw_files = request_obj.files.values()

        # Validation Checks
        self._set_ship_time()
        self.check_vetted_expired()
        self.update_vetted()

        # Save Organization in database
        self._save_org()

    def update_org(self, request_obj):
        form_data = dict(request_obj.form)

        # update Documents
        #TODO:

        # set data from form
        #TODO:

        # Checks
        self._set_ship_time()
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
        if self.raw_files:

            # Folder Config Settings
            os.chdir(db.UPLOAD_FOLDER)
            upload_folder = os.path.join(os.getcwd(),
                                        "organizations/suppliers/",
                                        self.organization_name)

            # create a file space in organization collections
            collection = {}
            collection.update({"files": []})

            for file in self.raw_files:
                # If the user does not select a file, the browser submits an
                # empty file without a filename.

                if file and db.allowed_file(file.filename):

                    # Compile file tree/path
                    filename = secure_filename(file.filename)
                    path = os.path.join(upload_folder, filename)

                    # Create file tree/path if it doesn't exist already
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                    # save Path to Documents
                    self.documents.append(path)

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

            for file in self.raw_files:
                # Save File
                file.save()

        # Commit and close session
        session.commit()
        session.close()
        return True

    def update_vetted(self):
        self.date_vetted = str(date.today())

    def check_vetted_expired(self):
        #TODO:
        self.vetted = True

    def _set_ship_time(self):
        if self.ship_time_unit == "Day/s":
            self.ship_time_in_days = self.ship_time
        elif self.ship_time_unit == "Week/s":
            self.ship_time_in_days = self.ship_time * 7
        elif self.ship_time_unit == "Month/s":
            self.ship_time_in_days = self.ship_time * 30
        else:
            self.ship_time_in_days = self.ship_time


@bp.route('/clients', methods=('GET', ))
@login_required
def clients():
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
        'Zim': ('Irk', 'Invader'),
        'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    session = mysqlx.get_session({
        'host': db.HOST,
        'port': db.PORT,
        'user': db.USER,
        'password': db.PASSWORD
    })
    result = session.sql(
        """SELECT * FROM `Organizations`.`Organizations`
        WHERE `Client` = true
        ORDER BY `Organization_Name` DESC;"""
    ).execute()
    g.orgtype = "client"
    clients_data = result.fetch_all()
    return render_template('organizations/read-org.html',
                           organizations=clients_data)

@bp.route('/suppliers', methods=('GET', ))
@login_required
def suppliers():
    session = mysqlx.get_session({
        'host': db.HOST,
        'port': db.PORT,
        'user': db.USER,
        'password': db.PASSWORD
    })
    result = session.sql(
        """SELECT * FROM `Organizations`.`Organizations`
        WHERE `Supplier` = true
        ORDER BY `Organization_Name` DESC;"""
    ).execute()
    g.orgtype = "supplier"
    suppliers_data = result.fetch_all()
    return render_template('organizations/read-org.html',
                           organizations=suppliers_data)


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
        if errors:
            for error in errors:
                flash(error)
        else:
            if org_type == "client":
                clients()
            else:
                suppliers()

    return render_template('organizations/create-org.html')


@bp.route('/update/<int:org_id>', methods=('GET', 'PUT'))
@login_required
def update(org_id):

    org = Organization()
    org.query_org(org_id)

    # Prevent prolifix entry from being edited.
    if org.organization_name == "Prolifix Nutrition":
        return render_template('home/index.html')

    if request.method == 'GET':
        if org.supplier:
            print("Update Client")
            return render_template('organizations/update-org.html',
                                   organizations=org.obj_to_dict())

    if request.method == 'PUT':
        org.update_org(request)
        errors = org.get_errors()

        # Flash Errors if any, else send data to db
        if errors:
            for error in errors:
                flash(error)

    if org.supplier:
        suppliers()
    elif org.client:
        clients()
    else:
        return render_template('home/index.html')
