import sqlalchemy as sa
from flask import current_app as app

def get_session():
    # Define the MariaDb engine using MariaDB Connector/Python
    host = app.config['DB_HOST']
    port = app.config['DB_PORT']
    user = app.config['DB_USER']
    password = app.config['DB_PASSWORD']

    engine = sa.create_engine(
            f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}',connect_args={'connect_timeout': 3}
        )
    
    Session = sa.orm.sessionmaker()
    Session.configure(bind=engine)
    Session = Session()
    return Session