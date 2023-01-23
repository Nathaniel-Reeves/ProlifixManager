"""
Handling api requests related to Organization objects.  Defines organization
objects.
"""

from flask import (
    Blueprint,
    flash,
    g,
    render_template,
    request,
    abort
)


from mrp_app.views.auth import (
    login_required
)
from flaskr.mrp_app.models.organizations import (
    Organization,
    fetch_suppliers,
    fetch_clients,
    fetch_documents
)
from mrp_app.models.people import (
    fetch_people_by_org
)


bp = Blueprint('organizations', __name__, url_prefix='/organizations')


@bp.route('/clients', methods=('GET', ))
@login_required
def get_clients(): 
    g.org_type = 'client'
    return render_template('organizations/read-org.html',
                           organizations=fetch_clients())

@bp.route('/suppliers', methods=('GET', ))
@login_required
def get_suppliers():
    g.org_type = 'supplier'
    return render_template('organizations/read-org.html',
                           organizations=fetch_suppliers())

@bp.route('/create/<string:org_type>', methods=('GET', 'POST', ))
@login_required
def post_organization(org_type):
    g.org_type = org_type

    if request.method == 'POST':
        form_data = dict(request.form)
        print(form_data)
        file_data = dict(request.files)
        print(file_data)

        new_org = Organization()
        if new_org.org_exists(request):
            flash("'%s' already exists in the database." % new_org.organization_name)
            flash("'%s' was NOT saved!" % new_org.organization_name)
        else:
            org_saved = new_org.post_org(request)
            errors = new_org.get_errors()

            # Flash Errors if any, else send data to db
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
    org = Organization()
    org.get_org(org_id)

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
    data = fetch_people_by_org(org_id)
    if data:
        return data
    abort(404)


@bp.route('/<int:org_id>/files', methods=('GET',))
@login_required
def get_documents(org_id):
    return fetch_documents(org_id)


