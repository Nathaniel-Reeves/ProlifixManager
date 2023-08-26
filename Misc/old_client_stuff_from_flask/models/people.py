from datetime import datetime
import mysqlx

from server.db import init_db


class Person:
    """Represents a person."""

    def __init__(self, person_id=None):
        self.errors = []

        # Person Attributes
        self.person_id = person_id
        self.first_name = ""
        self.last_name = ""
        self.job_title = ""
        self.phone_number = ""
        self.email_address = ""
        self.is_employee = None
        self.hourly_wage = 0
        self.contract_date = None
        self.termination_date = None

        if self.person_id and not self.first_name:
            self.get_person(self.person_id)

    def get_person(self, person_id):
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
            'Organizations').get_table('People')
        result = org_table.select().where(
            (f"person_id = '%s'") % str(person_id)).execute()
        session.close()
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
        self.first_name = data[result.index_of("first_name")]
        self.last_name = data[result.index_of("last_name")]
        self.job_title = data[result.index_of("job_title")]
        self.phone_number = data[result.index_of("phone_number")]
        self.email_address = data[result.index_of("email_address")]
        self.is_employee = data[result.index_of("is_employee")]
        self.hourly_wage = data[result.index_of("hourly_wage")]
        self.contract_date = data[result.index_of("contract_date")]
        self.termination_date = data[result.index_of("termination_date")]

        return True

def fetch_people_by_org(org_id):
    session = init_db()
    result = session.sql(
        """
        SELECT 
        `person_id`, 
        `first_name`,
        `last_name`,
        `job_description`,
        `department`,
        `phone_number_primary`,
        `email_address_primary` 
        FROM `Organizations`.`People`
        WHERE `organization_id` = %s
        ORDER BY `first_name`;
        """ % org_id
    ).execute()
    people_data = result.fetch_all()
    session.close()
    columns = result.get_columns()
    d = {}
    for data in people_data:
        res = {}
        for i in range(len(list(data))):
            res[columns[i].get_column_name()] = data[i]
        d[res["person_id"]] = res
    return d
