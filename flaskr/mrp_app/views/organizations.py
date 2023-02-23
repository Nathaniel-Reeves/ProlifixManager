"""
Handling api requests related to Organization objects.  Defines organization
objects.
"""
import json
from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    abort,
    jsonify
)

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

from mrp_app.views.auth import (
    login_required
)
from mrp_app.models.people import (
    fetch_people_by_org
)
from mrp_app.models.organizations import (
    Organization
)
from mrp_app.models.orders import (
    fetch_sales_by_org
)


@bp.route('/clients/json', methods=('GET', ))
@login_required
def get_clients(): 
    org = Organization()
    return jsonify(org.fetch_clients())

@bp.route('/suppliers/json', methods=('GET', ))
@login_required
def get_suppliers():
    org = Organization()
    return jsonify(org.fetch_suppliers())


@bp.route('/clients', methods=('GET', ))
@login_required
def show_clients():
    g.org_type = 'client'
    org = Organization()
    data = org.fetch_clients()
    return render_template("organizations/read-org.html")


@bp.route('/suppliers', methods=('GET', ))
@login_required
def show_suppliers():
    g.org_type = 'supplier'
    org = Organization()
    return render_template("organizations/read-org.html")


@bp.route('/<string:org_type>/create', methods=('GET', 'POST', ))
@login_required
def post_organization(org_type):
    g.org_type = org_type

    if request.method == 'POST':
        form_data = dict(request.form)
        file_data = dict(request.files)

        new_org = Organization()

        possible_duplicates = new_org.org_exists(
            form_data["organization_name"])
        if possible_duplicates:
            return jsonify({"possible_duplicates": possible_duplicates})
                
        else:
            org_saved = new_org.post_org(form_data)
            errors = new_org.get_errors()

            # Flash Errors if any, else send data to db
            if errors or (not org_saved):
                for error in errors:
                    flash(error)
                if not org_saved:
                    flash("You must specify if the organization is a supplier, client or both.")
                flash("'%s' was NOT saved!" % new_org)
            else:
                flash("'%s' was saved!" % new_org)

    return render_template("organizations/create-org.html")


@bp.route('/<int:org_id>/update', methods=('GET', 'PUT', 'POST', ))
@login_required
def put_organization(org_id):
    org = Organization(org_id)

    if request.method == 'GET':
        return jsonify(org.fetch_org())

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
            return jsonify(org.obj_to_dict())
        else:
            flash("Organization changes was saved!")
            return jsonify(org.obj_to_dict())

    if org.supplier:
        get_suppliers()
    elif org.client:
        get_clients()
    else:
        return render_template('home/index.html')
        

@bp.route('/<int:org_id>/people', methods=('GET',))
@login_required
def get_people(org_id):
    data = fetch_people_by_org(org_id)
    return jsonify(data)


@bp.route('/<int:org_id>/sales', methods=('GET',))
@login_required
def get_sales(org_id):
    data = fetch_sales_by_org(org_id)
    return data

@bp.route('/<int:org_id>/purchases', methods=('GET',))
@login_required
def get_purchases(org_id):
    # data = fetch_purchases_by_org(org_id)
    data = {}
    return data

@bp.route('/<int:org_id>/documents', methods=('GET',))
@login_required
def get_documents(org_id):
    org = Organization(org_id)
    return jsonify(org.fetch_documents())


