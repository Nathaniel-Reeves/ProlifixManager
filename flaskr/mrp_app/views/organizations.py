"""
Handling api requests related to Organization objects.  Defines organization
objects.
"""

import json
import mysqlx
from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
)
from werkzeug.utils import secure_filename


from mrp_app.views.auth import login_required
from mrp_app import app
from mrp_app.models.organizations import Organization


bp = Blueprint('organizations', __name__, url_prefix='/organizations')


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
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
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
        res = {"files": [],"personel":[]}
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
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
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
        res = {"files": [], "personel": [
            {"first_name": "dude", "last_name": "perfect"}]}
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


@bp.route('/<int:org_id>/people', methods=('GET',))
@login_required
def get_people(org_id):
    """Returns a list of people."""
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    result = session.sql(
        """
        SELECT `person_id`, 
        `first_name`,
        `last_name`,
        `job_title`,
        `phone_number`,
        `email_address` 
        FROM `Organizations`.`People`
        WHERE `organization_id` = %s
        ORDER BY `first_name`;
        """ % org_id
    ).execute()
    people_data = result.fetch_all()
    columns = result.get_columns()
    return_data = []
    for data in people_data:    
        res = {}
        for i in range(len(list(data))):
            res[columns[i].get_column_name()] = data[i]
        return_data.append(res)
    if return_data:
        return return_data
    abort(404)


@bp.route('/<int:org_id>/files', methods=('GET',))
@login_required
def get_documents(org_id):
    """Returns a list of people."""
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    doc = session.get_schema('Organizations').get_collection('Organizations').get_one(org_id).as_str()
    return json.loads(doc)

