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
        self.org_id = the organization id
        self.org_data = a dict containing organization data
        self.raw_files = a list containing files sent in by the client
        self.db_errors = a list contaning database errors
    """

    def __init__(self, organization_id=None):
        self.errors = []

        # Organization Attributes
        self.org_id = organization_id
        self.org_data = {"organization_id": self.org_id}
        self.raw_files = []
        self.db_errors = []

        # If organization_id query db
        if self.org_id:
            self.fetch_org()

    def __str__(self):
        return str(self.org_data)
    
    def fetch_org(self, org_id=None):
        if not org_id:
            org_id = self.org_id
        if self.org_data["organization_id"] != org_id or len(self.org_data) <= 1:
            session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
            result = session.sql(
                """SELECT
                    `organization_id`,
                    `organization_name`,
                    `organization_initial`,
                    `alias_name_1`,
                    `alias_name_2`,
                    `alias_name_3`,
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
                WHERE `organization_id` = {id};""".format(id = org_id)).execute()
            row = result.fetch_one()
            if row:
                self.org_data = self.org_row_to_dict(row)
                self.org_id = org_id
            session.close()
        return self.org_data

    def org_row_to_dict(self, row):
        data = {}
        data["organization_id"] = row["organization_id"]
        data["organization_name"] = row["organization_name"]
        data["organization_initial"] = row["organization_initial"]
        data["alias_name_1"] = row["alias_name_1"]
        data["alias_name_2"] = row["alias_name_2"]
        data["alias_name_3"] = row["alias_name_3"]
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
            `alias_name_1`,
            `alias_name_2`,
            `alias_name_3`,
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
        table = result.fetch_all()
        l = []
        for row in table:
            data = self.org_row_to_dict(row)
            l.append(data)
        session.close()
        return l
    
    def org_exists(self, org_name=None):
        if not org_name:
            return False
        session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
        clean = str(org_name).strip()
        result = session.sql(
            """CALL `Organizations`.ORG_EXISTS('%s')""" % (clean)).execute()
        columns = []
        for column in result.get_columns():
            columns.append(column.get_column_name())
        rows = result.fetch_all()
        l = []
        for row in rows:
            d = {}
            for col in columns:
                d[col] = row.get_string(col)
            l.append(d)
        session.close()
        return l

    def post_org(self, data):
        print(data)
        return False

    def get_errors(self):
        return self.errors


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
