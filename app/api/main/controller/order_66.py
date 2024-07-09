from view.response import CustomResponse, FlashMessage, error_message
import model as db
import sqlalchemy as sa
from flask import current_app as app

from sqlalchemy import select, update

def get_session():
    """
    Define the MariaDb engine using MariaDB Connector/Python.
    """
    host = app.config['DB_HOST']
    port = app.config['DB_PORT']
    user = app.config['DB_USER']
    password = app.config['DB_PASSWORD']

    engine = sa.create_engine(
            f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}',connect_args={'connect_timeout': 3}
        )

    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)
    Session.configure(autocommit=False)
    Session = Session()
    return Session

def execute_query(custom_response, stm):
    raw_data = []

    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response, raw_data, False

    # Execute the query
    try:
        stream = session.execute(stm)
        if isinstance(stm, sa.sql.selectable.Select):
            raw_data = stream.all()
        else:
            session.commit()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(400)
        session.close()
        return custom_response, raw_data, False

    session.close()
    return custom_response, raw_data, True

def order_66(request):
    custom_response = CustomResponse()

    # custom_response = fix_primary_name_id_column_organizations(custom_response)
    # custom_response = fix_primary_name_id_column_components(custom_response)

    if custom_response.status_code == 200:
        fm = FlashMessage(
            message='Success',
            title='Order 66'
        )
        print('SUCCESS')
        custom_response.insert_flash_message(fm)

    return custom_response

def fix_primary_name_id_column_components(custom_response):
    stm = select(db.Components)
    stm = stm.where(db.Components.primary_name_id == None)
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    for row in raw_data:
        stm = select(db.Component_Names)
        stm = stm.where(db.Component_Names.component_id == row[0].get_id())
        stm = stm.where(db.Component_Names.primary_name == True)
        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

        if raw_data:
            primary_name_id = raw_data[0][0].get_id()
        else:
            print("No primary name found for component_id: ", row[0].get_id())
            continue

        stm = update(db.Components) \
            .values(primary_name_id=primary_name_id) \
            .where(db.Components.component_id == row[0].get_id())

        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

    return custom_response

def fix_primary_name_id_column_organizations(custom_response):
    stm = select(db.Organizations)
    stm = stm.where(db.Organizations.primary_name_id == None)
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    for row in raw_data:
        stm = select(db.Organization_Names)
        stm = stm.where(db.Organization_Names.organization_id == row[0].get_id())
        stm = stm.where(db.Organization_Names.primary_name == True)
        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

        if raw_data:
            primary_name_id = raw_data[0][0].get_id()
        else:
            print("No primary name found for organization_id: ", row[0].get_id())
            continue

        stm = update(db.Organizations) \
            .values(primary_name_id=primary_name_id) \
            .where(db.Organizations.organization_id == row[0].get_id())

        custom_response, raw_data, success = execute_query(custom_response, stm)
        if not success:
            return custom_response

    return custom_response