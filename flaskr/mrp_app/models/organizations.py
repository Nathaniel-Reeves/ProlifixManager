import json
from datetime import date
import mysqlx
from mrp_app import app

# try:
#     from mrp_app import app
# except ImportError:
#     from mrp_app.models.substitute_App_class import App
#     app = App()
    

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
        self.org_id = organization_id
        self.org_data = {"organization_id": self.org_id}
        self.raw_files = []
        self.database_errors = []

        # If organization_id query db
        if self.org_id:
            self.fetch_org()

    def __str__(self):
        return str(self.org_data)
    
    def fetch_org(self, org_id=None):
        if not org_id:
            org_id = self.org_id
        if self.org_data["organization_id"] != org_id:
            session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
            result = session.sql(
                """SELECT
                    `organization_id`,
                    `organization_name`,
                    `organization_initial`,
                    `alias_names`,
                    `date_entered`,
                    `website_url`,
                    `vetted`,
                    `date_vetted`,
                    `risk_level`,
                    `supplier`,
                    `client`,
                    `lab`,
                    `other`,
                    `doc`,
                    `notes`
                FROM `Organizations`.`Organizations`
                WHERE `organization_id` = %s;""" % org_id).execute()
            session.close()
            row = result.fetch_one()
            if row:
                self.org_data = self.org_row_to_dict(row)
                self.org_id = org_id
        return self.org_data

    def org_row_to_dict(self, row):
        data = {}
        data["organization_id"] = row["organization_id"]
        data["organization_name"] = row["organization_name"]
        data["organization_initial"] = row["organization_initial"]
        data["alias_names"] = row["alias_names"]
        if row["date_entered"]:
            data["date_entered"] = date.fromisoformat(
                row["date_entered"])
        else:
            data["date_entered"] = None
        data["website_url"] = row["website_url"]
        data["vetted"] = row["vetted"]
        data["date_vetted"] = row["date_vetted"]
        data["risk_level"] = row["risk_level"].decode("utf-8")
        data["supplier"] = row["supplier"]
        data["client"] = row["client"]
        data["lab"] = row["lab"]
        data["other"] = row["other"]
        data["doc"] = json.loads(row["doc"].decode("utf-8"))
        data["notes"] = row["notes"]
        return data

    def fetch_clients(self):
        return self.fetch_orgs("client")
    
    def fetch_suppliers(self):
        return self.fetch_orgs("supplier")
        
    def fetch_orgs(self, org_roll):
        session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
        result = session.sql(
            """SELECT
            `organization_id`,
            `organization_name`,
            `organization_initial`,
            `alias_names`,
            `date_entered`,
            `website_url`,
            `vetted`,
            `date_vetted`,
            `risk_level`,
            `supplier`,
            `client`,
            `lab`,
            `other`,
            `doc`,
            `notes`
        FROM `Organizations`.`Organizations`
        WHERE %s = true
        ORDER BY `organization_name`;""" % org_roll
        ).execute()
        session.close()
        table = result.fetch_all()
        l = []
        for row in table:
            data = self.org_row_to_dict(row)
            l.append(data)
        return l
    
    def org_id_exists(self, org_id=None):
        if not org_id:
            if self.org_id:
                org_id = self.org_id
            else:
                return False
        session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
        result = session.sql(
            """SELECT
	            `organization_id`
            FROM `Organizations`.`Organizations`
            WHERE `organization_id` = %s;""" % org_id).execute()
        session.close()
        return result.has_data()



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
