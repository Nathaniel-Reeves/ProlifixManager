import sqlalchemy as sa
from flask import current_app as app

def get_session():
    # Define the MariaDb engine using MariaDB Connector/Python
    try:
        host = app.config['DB_HOSTNAME']
        port = app.config['DB_PORT']
        user = app.config['DB_USER']
        password = app.config['DB_PASSWORD']
    except:
        host = '192.168.1.133'
        port = 3306
        user = 'client'
        password = "ClientPassword!5"

    engine = sa.create_engine(
            f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}'
        )
    
    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)
    Session = Session()
    return Session