"""
Handling api requests related to Organization objects.  Defines organization
objects.
"""

import os
from datetime import date, datetime
import mysqlx
from flask import (Blueprint, flash, g, render_template, request,)
from werkzeug.utils import secure_filename

import json

from .auth import login_required
from ..db import db_conf as db

bp = Blueprint('organizations', __name__, url_prefix='/organizations')


class Organization:
    """Represents an organization or company.

    Contains company name and initials, address, website, and other
    information relevent to the needs of this MRP system.

    Attributes:
        organization_id (int): ID of the organization.
        organization_name (str): Name of the organization.
        organization_initial (str): Initials of the organization.
        date_entered (datetime): Date when the organization was entered.
        website (str): website for the organization.
        vetted (bool): True if the organization is vetted.
        date_vetted (datetime): Date when the organization was vetted.
        risk_level (int): Risk level of the organization.
        hq_street_address (str): HQ street address of the organization.
        hq_city (str): HQ city of the organization.
        hq_unit_apt (str): HQ unit/apt of the organization.
        hq_zip_code (str): HQ zip code of the organization.
        ship_time (str): Ship time of the organization.
        ship_time_unit (str): Ship time unit of the organization.
        ship_time_in_days (str): Ship time in days of the organization.
        prolifix (bool): True if the organization is a prolifix.
        supplier (bool): True if the organization is a supplier.
        client (bool): True if the organization is a client.
        documents (list): List of documents associated with the organization.
        notes (list): notes associated with the organization.
        TODO: files
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
        self.risk_level = 1
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

        self.raw_files = []

        # If organization_id query db
        if self.organization_id and not self.organization_name:
            self.get_org(self.organization_id)

    # """Error Handling Functions"""

    def get_errors(self):
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
        return self.errors

    def clear_errors(self):
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
        self.errors = []

    def print_errors(self):
        """Prints the errors found in the errors list."""
        for error in self.errors:
            print(error)
        self.clear_errors()

    # """Object Overide Functions"""

    def __str__(self):
        """String overide for printing the organization.

        Makes a readable version of the organization to help humans 
        read what this organization is representing.  Here is an example
        of what the output string might look like:

        <org_id = 1 | org_name = prolifix Nutrition | org_initial = PLX>

        Args:
            None

        Returns:
            A string representing key information about this organization.

        Raises:
            TODO:
        """
        return_str = "<"
        return_str += "org_id = " + str(self.organization_id) + " | "
        return_str += "org_name = " + str(self.organization_name) + " | "
        return_str += "org_initial = " + str(self.organization_initial)
        return_str += ">"
        return return_str

    def __dict__(self):
        """Object Overide for making a dictionary representation of the 
        organization.

        Args:
            None

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each column is represented as a key value pair. For
            example:

            {'Serak': ('Rigel VII', 'Preparer'),
            'Zim': ('Irk', 'Invader'),
            'Lrrr': ('Omicron Persei 8', 'Emperor')}

            If a key from the keys argument is missing from the dictionary,
            then that row was not found in the table.

        Raises:
            TODO: 
        """
        return self.obj_to_dict()

    # """Restful API Functions"""

    def get_org(self, org_id):
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
        # Connect to db and query organization data
        session = self._connect_session()
        org_table = session.get_schema(
            'Organizations').get_table('Organizations')
        result = org_table.select().where(
            (f"organization_id = '%s'") % str(org_id)).execute()
        encoded_data = result.fetch_one()

        # Decode byte objects to str objects
        data = []
        for i in encoded_data:
            if type(i) == bytes:
                data.append(i.decode('UTF-8'))
            elif type(i) == datetime:
                data.append(i.date())
            else:
                data.append(i)

        # Save table data into self from db
        self.organization_id = data[result.index_of("organization_id")]
        self.organization_name = data[result.index_of("organization_name")]
        self.organization_initial = data[result.index_of(
            "organization_initial")]
        self.date_entered = data[result.index_of("date_entered")]
        self.website = data[result.index_of("website")]
        self.vetted = data[result.index_of("vetted")]
        self.date_vetted = data[result.index_of("date_vetted")]
        self.risk_level = data[result.index_of("risk_level")]
        self.hq_street_address = data[result.index_of("hq_street_address")]
        self.hq_unit_apt = data[result.index_of("hq_unit_apt")]
        self.hq_city = data[result.index_of("hq_city")]
        self.hq_region = data[result.index_of("hq_region")]
        self.hq_country = data[result.index_of("hq_country")]
        self.hq_zip_code = data[result.index_of("hq_zip_code")]
        self.ship_time = data[result.index_of("ship_time")]
        self.ship_time_unit = data[result.index_of(
            "ship_time_unit")]
        self.ship_time_in_days = data[result.index_of("ship_time_in_days")]
        self.prolifix = data[result.index_of("prolifix")]
        self.supplier = data[result.index_of("supplier")]
        self.client = data[result.index_of("client")]
        self.notes = data[result.index_of("notes")]

        # get organization document data from db
        self._get_org_docs(org_id)

        return True

    def put_org(self, request_obj):
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
        self._set_data(request_obj)

        # Start session and transaction
        session = self._connect_session()
        session.start_transaction()

        # Get table
        org_table = session.get_schema(
            'Organizations').get_table('Organizations')

        # Prepare update object
        obj_data = self.obj_to_dict()
        update_obj = org_table.update()
        for key in obj_data:
            update_obj = update_obj.set(key, obj_data[key])

        # Execute update
        result = update_obj.where("organization_id == %s" %
                                self.organization_id).limit(1).execute()

        # Handle errors, commit/rollback and close session
        if self._check_errors(result):
            session.rollback()
            session.close()
            self.print_errors()
            return False
        session.commit()
        session.close()
        return True

    def post_org(self, request_obj):
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

        self._set_data(request_obj)

        # Start session and transaction
        session = self._connect_session()
        session.start_transaction()

        # Get table

        # Get schema & table
        org_schema = session.get_schema('Organizations')
        org_table = org_schema.get_table('Organizations')
        self.organization_id = org_table.count() + 1

        # Prepare Data
        obj_data = self.obj_to_dict()
        columns = list(obj_data.keys())
        values = list(obj_data.values())

        # Prepare insert statement and execute
        result = org_table.insert(columns).values(values).execute()

        # Handle errors, continue/rollback and close session
        if self._check_errors(result, "INSERT TO TABLE ERR"):
            session.rollback()
            session.close()
            self.print_errors()
            return False

        # Save Uploaded Files
        if self.raw_files:

            # Folder Config Settings
            os.chdir(db.UPLOAD_FOLDER)
            upload_folder = os.path.join(os.getcwd(), "organizations/",self.organization_name)

            # create a file space in organization collections
            files = {"_id":self.organization_id,"files":[]}

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
                    files["files"].append({
                        "date_uploaded": str(datetime.today()),
                        "file_path": path,
                        "file_name": filename
                    })

            # Create Collection if none exists
            #org_coll = org_schema.create_collection('OrganizationDocs', True)

            # Get Collection
            org_coll = org_schema.get_collection('Organizations',
                                                 check_existence=True)

            print(json.dumps(files))

            # Save file paths
            result = org_coll.modify('_id = %s' % self.organization_id).patch(files).execute()

            # Handle errors, continue/rollback and close session
            if self._check_errors(result, "INSERT DOCS ERR"):
                session.rollback()
                session.close()
                self.print_errors()
                return False

            for file in self.raw_files:
                # Compile file tree/path
                filename = secure_filename(file.filename)
                path = os.path.join(upload_folder, filename)
                # Save File
                file.save(path)
                file.close()

        # Commit and close session
        session.commit()
        session.close()
        return True

    # """Helper Functions"""
    def org_exists(self, request_obj):
        """
        Checks if the organization exists in the database.

        Returns:
            bool: True if the organization exists, False otherwise.
        """
        self._set_data(request_obj)
        session = self._connect_session()
        result = session.sql("""
        SELECT EXISTS (SELECT * FROM `Organizations`.`Organizations` WHERE `organization_name` = "%s");""" % self.organization_name).execute()
        return result.fetch_one()[0]

    def obj_to_dict(self):
        """Fetches organization documents

        Retrieves organization documents using the references provided 
        by the database.

        Args:
            org_id (str): The unique identifier of the organization.

        Returns:
            bool: True on success, otherwise False.

        Raises:
            IOError: An error occurred accessing the documents.
        """
        return_dict = {}
        return_dict["organization_id"] = self.organization_id
        return_dict["organization_name"] = self.organization_name
        return_dict["organization_initial"] = self.organization_initial
        #return_dict["date_entered"] = self.date_entered
        return_dict["website"] = self.website
        return_dict["vetted"] = self.vetted
        return_dict["date_vetted"] = self.date_vetted
        return_dict["risk_level"] = self.risk_level
        return_dict["hq_street_address"] = self.hq_street_address
        return_dict["hq_unit_apt"] = self.hq_unit_apt
        return_dict["hq_city"] = self.hq_city
        return_dict["hq_region"] = self.hq_region
        return_dict["hq_country"] = self.hq_country
        return_dict["hq_zip_code"] = self.hq_zip_code
        return_dict["ship_time"] = self.ship_time
        return_dict["ship_time_unit"] = self.ship_time_unit
        return_dict["ship_time_in_days"] = self.ship_time_in_days
        return_dict["prolifix"] = self.prolifix
        return_dict["supplier"] = self.supplier
        return_dict["client"] = self.client
        return_dict["notes"] = self.notes
        return return_dict
        
    def _get_org_docs(self, org_id):
        """Fetches organization documents

        Retrieves organization documents using the references provided 
        by the database.

        Args:
            org_id (str): The unique identifier of the organization.

        Returns:
            bool: True on success, otherwise False.

        Raises:
            IOError: An error occurred accessing the documents.
        """
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

    def _connect_session(self):
        session = mysqlx.get_session({
            'host': db.HOST,
            'port': db.PORT,
            'user': db.USER,
            'password': db.PASSWORD
        })
        return session

    def _check_errors(self, result_obj, err_message):
        # Save Statement Results
        warnings = result_obj.get_warnings()
        rows_effected = result_obj.get_affected_items_count()

        # IF Err, create report
        if warnings != [] and rows_effected != 1:
            error = err_message + " \n"
            error += "Warnings: \n"
            for warning in warnings:
                error += ("    W:" + warning + "\n")
                error += "Attempted Rows Effected: " + rows_effected + "\n"
                error += "Expected Rows Effected: 1 \n"
                self.errors.append(error)
            return True
        return False

    def _set_data(self, request_obj):
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
        request_data = request_obj.form
        flag_type = True
        # prolifix record cannot be edited on the client side.
        if "prolifix" in request_data:
            return False

        if "supplier" in request_data:
            self.supplier = request_data["supplier"]
            flag_type = False

        if "client" in request_data:
            self.client = request_data["client"]
            flag_type = False

        if flag_type:
            return False

        if "organization_id" in request_data:
            self.organization_id = request_data["organization_id"]

        self.date_entered = str(date.today())
        self.organization_name = request_data["organization_name"]
        self.organization_initial = request_data["organization_initial"]
        self.website = request_data["website"]
        self.date_vetted = request_data["date_vetted"]
        self.risk_level = request_data["risk_level"]
        self.hq_street_address = request_data["hq_street_address"]
        self.hq_unit_apt = request_data["hq_unit_apt"]
        self.hq_city = request_data["hq_city"]
        self.hq_region = request_data["hq_region"]
        self.hq_country = request_data["hq_country"]
        self.hq_zip_code = request_data["hq_zip_code"]
        self.ship_time = request_data["ship_time"]
        self.ship_time_unit = request_data["ship_time_unit"]
        self.notes = request_data["notes"]

        # set Documents
        if request_obj.files:
            self.raw_files = list(request_obj.files.values())
        else:
            self.raw_files = []

        # Validation Checks
        self._set_ship_time()
        self.check_vetted_expired()
        self.update_vetted()

    def update_vetted(self):
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
        self.date_vetted = str(date.today())

    def check_vetted_expired(self):
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
        #TODO:
        self.vetted = True

    def _set_ship_time(self):
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
        if self.ship_time_unit == "Day/s":
            self.ship_time_in_days = int(self.ship_time)
        elif self.ship_time_unit == "Week/s":
            self.ship_time_in_days = int(self.ship_time) * 7
        elif self.ship_time_unit == "Month/s":
            self.ship_time_in_days = int(self.ship_time) * 30
        else:
            self.ship_time_in_days = 0

@bp.route('/clients', methods=('GET', ))
@login_required
def get_clients():
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
        WHERE `client` = true
        ORDER BY `organization_name` DESC;"""
    ).execute()
    g.org_type = "client"
    clients_data = result.fetch_all()
    columns = result.get_columns()
    return_data = []
    for data in clients_data:
        res = {"files": []}
        for i in range(len(list(data))):
            if columns[i].get_column_name() == "doc":
                res["files"] = json.loads(data[i].decode(
                    'utf8').replace("'", '"'))["files"]
            else:
                res[columns[i].get_column_name()] = data[i]
        return_data.append(res)
    return render_template('organizations/read-org.html',
                           organizations=return_data)

@bp.route('/suppliers', methods=('GET', ))
@login_required
def get_suppliers():
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
        WHERE `supplier` = true
        ORDER BY `organization_name` DESC;"""
    ).execute()
    g.org_type = "supplier"
    suppliers_data = result.fetch_all()
    columns = result.get_columns()
    return_data = []
    for data in suppliers_data:
        res = {"files":[]}
        for i in range(len(list(data))):
            if columns[i].get_column_name() == "doc":
                res["files"] = json.loads(data[i].decode(
                    'utf8').replace("'", '"'))["files"]
            else:
                res[columns[i].get_column_name()] = data[i]
        return_data.append(res)
    return render_template('organizations/read-org.html',
                           organizations=return_data)

@bp.route('/create/<string:org_type>', methods=('GET', 'POST', ))
@login_required
def post_organization(org_type):
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

    # Stop new entry for prolifix
    if org_type == "prolifix":
        return render_template('organizations/create-org.html')

    g.org_type = org_type

    if request.method == 'POST':
        new_org = Organization()
        if new_org.org_exists(request):
            flash("'%s' already exists in the database." % new_org.organization_name)
            flash("'%s' was NOT saved!" % new_org.organization_name)
        else:
            org_saved = new_org.post_org(request)
            errors = new_org.get_errors()

            # Flash Erros if any, else send data to db
            if errors or (not org_saved):
                for error in errors:
                    flash(error)
                if not org_saved:
                    flash("You must specify if the organization is a supplier, client or both.")
                flash("'%s' was NOT saved!" % new_org.organization_name)
            else:
                flash("'%s' was saved!" % new_org.organization_name)

    return render_template('organizations/create-org.html')

@bp.route('/update/<int:org_id>', methods=('GET', 'PUT', 'POST', ))
@login_required
def put_organization(org_id):
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

    org = Organization()
    org.get_org(org_id)

    # Prevent prolifix entry from being edited.
    if org.prolifix:
        flash("See IT Manager to edit Prolifix company Details.")
        return render_template('home/index.html')

    if request.method == 'GET':
        return render_template('organizations/update-org.html',
                                   organization_data=org.obj_to_dict())

    if request.method == 'POST':
        org_saved = org.put_org(request)
        errors = org.get_errors()

        # Flash Erros if any, else send data to db
        if errors or (not org_saved):
            for error in errors:
                flash(error)
            if not org_saved:
                flash(
                    "You must specify if the organization is a supplier, client or both.")
            flash("Organization changes were not saved!")
            return render_template('organizations/update-org.html',
                                   organization_data=org.obj_to_dict())
        else:
            flash("Organization changes was saved!")
            return render_template('organizations/update-org.html',
                                   organization_data=org.obj_to_dict())

    if org.supplier:
        get_suppliers()
    elif org.client:
        get_clients()
    else:
        return render_template('home/index.html')

