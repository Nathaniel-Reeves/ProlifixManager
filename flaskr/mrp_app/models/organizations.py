
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
    information relevent to the needs of this MRP system regarding
    organizations.

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
        self.organization_data = {}
        self.raw_files = []
        self.database_errors = []

        # If organization_id query db
        if self.organization_id:
            self.fetch_org()
    
    def fetch_org(self, org_id=None):
        if not org_id:
            org_id = self.organization_id
        if not self.organization_data:
            session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
            result = session.sql(
                """SELECT * FROM `Organizations`.`Organizations`
                WHERE `organization_id` = %s
                ORDER BY `organization_name`;""" % org_id).execute()
            self.organization_data = result.fetch_all()[0]
            print(type(self.organization_data))
            self.organization_id = org_id
        return self.organization_data






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
