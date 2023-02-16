import json
from datetime import datetime
import mysqlx

try:
    from mrp_app import app
except ImportError:
    print("Import app failure, Importing from Substitute Class")
    from mrp_app.models.substitute_App_class import App
    app = App()
    

class Organization:

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
                    `date_entered`,
                    `website_url`,
                    `risk_level`,
                    `supplier`,
                    `client`,
                    `lab`,
                    `other`,
                    `doc`,
                    `notes`
                FROM `Organizations`.`org_primary`
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
        if row["date_entered"]:
            data["date_entered"] = datetime.date(
                row["date_entered"]).isoformat()
        else:
            data["date_entered"] = None
        data["website_url"] = row["website_url"]
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
            `date_entered`,
            `website_url`,
            `date_vetted`,
            `risk_level`,
            `supplier`,
            `client`,
            `lab`,
            `other`,
            `doc`,
            `notes`
        FROM `Organizations`.`org_primary`
        WHERE %s = true
        ORDER BY `organization_name`;""" % org_roll
        ).execute()
        table = result.fetch_all()
        d = {}
        for row in table:
            data = self.org_row_to_dict(row)
            d[data["organization_id"]] = data
        session.close()
        return d
    
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

    def fetch_documents(self):
        return self.org_data["doc"]

