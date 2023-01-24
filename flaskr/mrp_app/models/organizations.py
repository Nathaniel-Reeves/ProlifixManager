
import os
import json
from datetime import date, datetime
import mysqlx
from werkzeug.utils import secure_filename


from mrp_app import app
from mrp_app.models.db import allowed_file


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
        supplier (bool): True if the organization is a supplier.
        client (bool): True if the organization is a client.
        lab (bool): True if the organization is a lab.
        other (bool): True if the organization some other catagory.
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
        self.supplier = False
        self.client = False
        self.lab = False
        self.other = False
        self.documents = []
        self.notes = ""

        self.raw_files = []

        # If organization_id query db
        if self.organization_id and not self.organization_name:
            self.get_org(self.organization_id)

    # """Error Handling Functions"""

    def get_errors(self):
        return self.errors

    def clear_errors(self):
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

        <org_id = 1 | org_name = Prolifix Nutrition | org_initial = PLX>

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
        self.organization_name = data[result.index_of("organization_name")].strip()
        self.organization_initial = data[result.index_of(
            "organization_initial")]
        self.date_entered = data[result.index_of("date_entered")]
        self.website = data[result.index_of("website")].strip()
        self.vetted = data[result.index_of("vetted")]
        self.date_vetted = data[result.index_of("date_vetted")]
        self.risk_level = data[result.index_of("risk_level")]
        self.hq_street_address = data[result.index_of(
            "hq_street_address")].strip()
        self.hq_unit_apt = data[result.index_of("hq_unit_apt")].strip()
        self.hq_city = data[result.index_of("hq_city")].strip()
        self.hq_region = data[result.index_of("hq_region")].strip()
        self.hq_country = data[result.index_of("hq_country")].strip()
        self.hq_zip_code = data[result.index_of("hq_zip_code")].strip()
        self.ship_time = data[result.index_of("ship_time")]
        self.ship_time_unit = data[result.index_of(
            "ship_time_unit")]
        self.ship_time_in_days = data[result.index_of("ship_time_in_days")]
        self.supplier = data[result.index_of("supplier")]
        self.client = data[result.index_of("client")]
        self.documents = json.loads(data[result.index_of("doc")])["files"]
        self.notes = data[result.index_of("notes")]


        return True

    def put_org(self, request_obj):
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
        if self._check_errors(result, "DB Err"):
            session.rollback()
            session.close()
            self.print_errors()
            return False
        session.commit()
        session.close()
        return True

    def post_org(self, request_obj):

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
            os.chdir(app.config["UPLOAD_FOLDER"])
            upload_folder = os.path.join(os.getcwd(), "organizations/",self.organization_name)

            # create a file space in organization collections
            files = {"_id":self.organization_id,"files":[]}

            for file in self.raw_files:
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                

                if file and allowed_file(file.filename):

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
                        "full_file_path": path,
                        "local_file_path": os.path.join("organizations/", self.organization_name, filename),
                        "file_name": filename,
                        "organizaiton_name": self.organization_name
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
        return_dict["supplier"] = self.supplier
        return_dict["client"] = self.client
        #return_dict["documents"] = self.documents
        return_dict["notes"] = self.notes
        return return_dict
        
    def _connect_session(self):
        session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
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
        request_data = request_obj.form
        flag_type = True

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
        # TODO:
        self.date_vetted = str(date.today())

    def check_vetted_expired(self):
        # TODO:
        self.vetted = True

    def _set_ship_time(self):
        # TODO:
        if self.ship_time_unit == "Day/s":
            self.ship_time_in_days = int(self.ship_time)
        elif self.ship_time_unit == "Week/s":
            self.ship_time_in_days = int(self.ship_time) * 7
        elif self.ship_time_unit == "Month/s":
            self.ship_time_in_days = int(self.ship_time) * 30
        else:
            self.ship_time_in_days = 0


def fetch_clients():
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    result = session.sql(
        """SELECT * FROM `Organizations`.`Organizations`
        WHERE `client` = true
        ORDER BY `organization_name`;"""
    ).execute()
    clients_data = result.fetch_all()
    clients_columns = result.get_columns()
    data = table_to_json(clients_data, clients_columns)
    return data


def fetch_suppliers():
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    result = session.sql(
        """SELECT * FROM `Organizations`.`Organizations`
        WHERE `supplier` = true
        ORDER BY `organization_name`;"""
    ).execute()
    suppliers_data = result.fetch_all()
    suppliers_columns = result.get_columns()
    data = table_to_json(suppliers_data, suppliers_columns)
    return data

def table_to_json(table_data, columns):
    return_data = []
    for row_data in table_data:
        res = {"files": []}
        for i in range(len(list(row_data))):
            if columns[i].get_column_name() == "doc":
                res["files"] = json.loads(row_data[i].decode(
                    'utf8').replace("'", '"'))["files"]
            else:
                res[columns[i].get_column_name()] = row_data[i]
        return_data.append(res)
    return return_data

def fetch_documents(org_id):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    doc = session.get_schema('Organizations').get_collection(
        'Organizations').get_one(org_id).as_str()
    return json.loads(doc)


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
